"""
USB Protocol defined for Firmware-STM32F103-DRV8870

I'm planing to use JSON as standard transmission object for
the protocol, 
JSON format works better because it has quite good 
resistivity to malformed commands, 
and it is significantly more flexible than line-based
structure. 
But most c-based JSON parsers have serious performance
problem when handling large array conversions, 
so I'll just keep using line-based protocol for now.

To prevent arbitrary writes from other software, 
commands must start with specific header and tail to 
take effect (which should not be necessary if other 
companies design their products responsibly).

Reponses sent from the device do not need the tail or header.

Packet structure:

    HEADER      ? bytes             An arbitrary sequence for validation
                                     if mismatch, command is ignored
    SIZE        2 bytes             0-65536, representing how many bytes
                                     to expect until TAIL
    COMMAND     1 byte              0-256, one of the supported commands
    CONTENT     (SIZE - 1) bytes    Additional params required by COMMAND
    GARBAGE     ? bytes             If these bytes exist, command is
                                     ignored
    TAIL        ? bytes             An arbitrary sequence for validation
                                     this triggers command validation and
                                     execution

The device recieves message and stores the stream in a cyclic buffer 
continuously,
whenever the device detected a TAIL pattern, it interupts to consume the
command in buffer. The header is now checked, and if mismatch, the current
command is ignored and error reported.

H = Header Byte
S = Size Byte
C = Command Byte
X = Content Byte
G = Garbage Byte, Garbage inserted to buffer because transmission
     error or other software accidental write
T = Tail Byte

BUFFER: ------------------------------------------------------------------
        HHHSSCXXXTTTHHHSSCTTTGGGGGGHHHSSCXXXXXXXXXXTTTHHHSSCXXXXXGGGGGTTTH
        |<-------->|<------>||<---><---------------->||<--------------->|
        |<---------Consume  ||<----------------------Consume            |
                   |<-------Consume                   |<----------------Consume
        |  Normal Commands  || Discarded Command due ||Discarded Command|
                             | to mismatched header  ||due to garbage in|
                                                     ||command body     |

"""

# Just using some arbitrary numbers as header and tail
# header = 114514
# tail = 1919810
import serial
from threading import Thread
import struct
import time


USB_COMMAND_HEADER = [0x01, 0x01, 0x04, 0x05, 0x01, 0x04]
USB_COMMAND_TAIL = [0x01, 0x09, 0x01, 0x09, 0x08, 0x01, 0x00]
# USB commands
"""
2 bytes, device reports all status of given channel
Bytes: 00000001  CHCHCHCH
       Command   Channel
"""
USB_COMMAND_REPORT_STATUS = [0x01]

"""
6 bytes, set target for device, two's complement
Bytes: 00000010  CHCHCHCH  HHHHHHHH  HHHHHHHH  LLLLLLLL  LLLLLLLL
       Command   Channel   [High 16         ]  [Low 16          ]
                           [Target (32-bit)                     ]
"""
USB_COMMAND_SET_TARGET = [0x02]

"""
14 bytes, update PID parameters on device
Data format: two's complement q31 fixed point numbers
    We use q31 format because these parameters should be relatively small,
    so no loss of precision should happen during transmission.
    the q31 format is converted to float point numbers at device end,
    because we are not using q31 implementation of PID controller
    (we are currently using a float point (float32) implementation)
    
Bytes: 00000011  CHCHCHCH  HHHHHHHH  HHHHHHHH  LLLLLLLL  LLLLLLLL  HHHHHHHH  HHHHHHHH  LLLLLLLL  LLLLLLLL  HHHHHHHH  HHHHHHHH  LLLLLLLL  LLLLLLLL
       Command   Channel   [High 16         ]  [Low 16          ]  [High 16         ]  [Low 16          ]  [High 16         ]  [Low 16          ]
                           [P (32-bit)                          ]  [I (32-bit)                          ]  [D (32-bit)                          ]

Take P as example, P_set =  P / 2147483648 * scale 
P is passed to device with little-endian format.
"""
USB_COMMAND_SET_PID_PARAMETERS = [0x03]

"""
3 bytes, set channel output mode to selected mode.
Bytes: 00000100  CHCHCHCH  SSSSSSSS
       Command   Channel   Switch
Switch = 00000000 to use forced output mode (open loop PWM), MCU ignores all PID parameters and output duty cycle tracks target. 
Switch = 00000001 to use velocity loop PID mode (measured velocity tracks target),
Switch = 00000002 to use position loop PID mode (measured position tracks target)

NOTE: when changing modes, motor speed is automatically set to 0, but not for motor position.
"""
USB_COMMAND_SET_WORKING_MODE = [0x04]

"""
2 bytes, device reports current parameters stored in RAM
Bytes: 00000101  CHCHCHCH
       Command   Channel
"""
USB_COMMAND_REPORT_PARAMETERS = [0x05]
# Enumerates

SERVO_MODE_OPEN_LOOP = 0x00
SERVO_MODE_VELOCITY_LOOP = 0x01
SERVO_MODE_POSITION_LOOP = 0x02


# Header to identify report type
"""
Status report,
Bytes: 1 * 2 + 4 * 6 + 1 = 27
Big-endian (n = buf[0] << 24 + buf[1] << 16 + buf[2] << 8 + buf[3])

0           1           2           3           4           5       
00000000    CHCHCHCH    HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL
Type        Channel     [Position (int32)                          ]

6           7           8           9           10          11          12          13      
HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL    HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL  
[Velocity (int32)                          ]    [Target (int32)                            ]  

15          15          16          17          18          19          20          21      
HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL    HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL  
[Output P Clock Cycles (int32)             ]    [Output N Clock Cycles (int32)             ]  

22          23          24          25          26
HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL    MODEMODE
[Output PWM Period Clock Cycles (int32)    ]    Servo Mode
"""
USB_REPORT_STATUS = 0x00
LENGTH_USB_REPORT_STATUS = 27

"""
Parameter or mode set OK (Acknowledge)
Bytes: 00000001
"""
USB_REPORT_OK = 0x01

"""
Parameter or mode set error (Exception)
Bytes: 00000010  RRRRRRRR--????????
       Type      [Reason (N Bytes)]
"""
USB_REPORT_ERROR = 0x02

"""
report current parameter values loaded into RAM
Bytes: 1 * 2 + 4 * 5 = 22
Big-endian, scaled q31, two's complement representation
n = struct.unpack('>1i', buf) / 2147483648 * scale

0           1           2           3           4           5       
00000011    CHCHCHCH    HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL  
Type        Channel     [P (32-bit)                                ]

6           7           8           9           10          11          12          13
HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL    HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL
[I (32-bit)                                ]    [D (32-bit)                                ]

14          15          16          17          18          19          20          21
HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL    HHHHHHHH    HHHHHHHH    LLLLLLLL    LLLLLLLL
[tau (32-bit)                              ]    [T (32-bit)                                ]
"""
USB_REPORT_PARAMETERS = 0x03
LENGTH_USB_REPORT_PARAMETERS = 22



class DRV8870:
    def __init__(self, com='COM5') -> None:
        self.com = com
        self.commands_buffer = list()
        self.messages_from_device_buffer = list()
        self.status = {}
        self.parameters = {}
        self.new_status_available = False
        self.parameters_updated_from_device = False

    def start(self):
        # clear buffers before start to communicate
        self.commands_buffer = list()
        self.messages_from_device_buffer = list()
        self.serial_manager_thread = Thread(target=self.serial_task)
        self.serial_manager_thread_running = True
        self.serial_manager_thread.start()
        self.message_handler_thread = Thread(target=self.message_handler_task)
        self.message_handler_thread_running = True
        self.message_handler_thread.start()

    def shutdown(self):
        self.serial_manager_thread_running = False
        self.message_handler_thread_running = False
        # we need enough time to make sure all connections are disconnected
        # so that we can gracefully exit main thread.
        time.sleep(1)

    def serial_task(self):
        """
        This single thread manages all serial I/O with the device
        This prevents write order problem when using multiple threads,
        while facilitates message reading.
        """
        self.ser = serial.Serial(self.com, baudrate=115200, timeout=1)
        while self.serial_manager_thread_running:
            time.sleep(0.01)  # This prevents pyserial eating up all CPU
            if self.ser.in_waiting:
                new_message = self.ser.read_all()
                self.messages_from_device_buffer.append(new_message)
            if len(self.commands_buffer) != 0:
                to_send = self.commands_buffer.pop(0)
                self.ser.write(to_send)

        self.ser.close()

    def message_handler_task(self):
        """
        This thread is responsible to handle all messages coming from
        the device.
        """
        while self.message_handler_thread_running:
            time.sleep(0.01)
            if len(self.messages_from_device_buffer) != 0:
                try:
                    earliest_message = self.messages_from_device_buffer.pop(0)
                    self.parse_message(earliest_message)
                    self.new_data_available = True
                except ValueError as e:
                    print("Error parsing message.", e)

    def stream_command(self, command: list[int]):
        command_length = len(command)
        assert command_length < 65536, "Command length must be within 0 - 65535"
        to_send = USB_COMMAND_HEADER + \
            [(command_length >> 8) % 256, command_length % 256] + \
            command + USB_COMMAND_TAIL
        bytes_length = len(to_send)
        to_send = struct.pack('{}B'.format(bytes_length), *to_send)
        self.commands_buffer.append(to_send)

    def parse_message(self, message_raw: bytes):
        """
        Parse report according to protocol, raises ValueError if
        a match is not found
        """
        msg_len = len(message_raw)
        print(message_raw)
        # NOTE: Python3 automatically decodes bytes object to ints if only
        #       1 byte is accessed via [], this is non-consistent with [:]
        #       For example:
        #           >>> b'\x01\x02\x03\x04'[0]
        #           1
        #           >>> b'\x01\x02\x03\x04'[0:2]
        #           b'\x01\x02'
        #       So we do not need to struct.unpack here if only 1 byte is to
        #           be unpacked.
        # report_type = struct.unpack('1B', message_raw[0])
        report_type = message_raw[0]
        if report_type == USB_REPORT_STATUS:
            print("Device reported a new status.")
            if msg_len < LENGTH_USB_REPORT_STATUS:
                raise ValueError(
                    (
                        "Status message length is shorter than defined value"
                        " {message_length}, maybe we missed some data here."
                    ).format(message_length=msg_len))
            elif msg_len == LENGTH_USB_REPORT_STATUS:
                self.parse_status_report(message_raw)
            else:
                self.parse_status_report(
                    message_raw[0:LENGTH_USB_REPORT_STATUS])
                self.parse_message(message_raw[LENGTH_USB_REPORT_STATUS:])
        elif report_type == USB_REPORT_OK:
            print("Device reported OK.")
        elif report_type == USB_REPORT_ERROR:
            if msg_len == 1:
                print("Device reported ERROR.")
            else:
                print("Device reported ERROR, reason: ", message_raw[1:])
        elif report_type == USB_REPORT_PARAMETERS:
            print("Device reported current parameter.")
            if msg_len < LENGTH_USB_REPORT_PARAMETERS:
                raise ValueError(
                    (
                        "Parameter report message length is shorter than defined value"
                        " {message_length}, maybe we missed some data here."
                    ).format(
                        message_length=msg_len)
                )
            elif msg_len == LENGTH_USB_REPORT_PARAMETERS:
                self.parse_parameters_report(message_raw)
            else:
                self.parse_parameters_report(
                    message_raw[0:LENGTH_USB_REPORT_PARAMETERS])
                self.parse_message(message_raw[LENGTH_USB_REPORT_PARAMETERS:])
        else:
            raise ValueError("Not supported report type.")
        # print(status)

    def parse_status_report(self, message_raw: bytes):
        """
        status message format: see above constant definition section.
        """
        # channel does not to be unpacked because it is only 1 byte, see above
        # explanation in parse_message
        channel = str(message_raw[1])  # channel is guaranteed to be int
        position = struct.unpack('>1i', message_raw[2:6])[0]
        velocity = struct.unpack('>1i', message_raw[6:10])[0]
        target = struct.unpack('>1i', message_raw[10:14])[0]
        output_p = struct.unpack('>1i', message_raw[14:18])[0]
        output_n = struct.unpack('>1i', message_raw[18:22])[0]
        pwm_period = struct.unpack('>1i', message_raw[22:26])[0]
        working_mode = message_raw[26]
        if channel in self.status:
            pass
        else:
            self.status[channel] = dict()
        self.status[channel]["Position"] = position
        self.status[channel]["Velocity"] = velocity
        self.status[channel]["Target"] = target
        self.status[channel]["OutputP"] = output_p
        self.status[channel]["OutputN"] = output_n
        self.status[channel]["OutputPeriod"] = pwm_period
        self.status[channel]["WorkingMode"] = working_mode
        self.new_status_available = True

    def parse_parameters_report(self, message_raw: bytes):
        """
        parameters message format: see above constant definition section.
        report current parameter values loaded into RAM
        """
        # channel does not to be unpacked because it is only 1 byte, see above
        # explanation in parse_message
        channel = str(message_raw[1])  # channel is guaranteed to be int
        p_q31 = struct.unpack('>1i', message_raw[2:6])[0]
        pid_p = p_q31 / 2147483648 * 10
        i_q31 = struct.unpack('>1i', message_raw[6:10])[0]
        pid_i = i_q31 / 2147483648 * 10
        d_q31 = struct.unpack('>1i', message_raw[10:14])[0]
        pid_d = d_q31 / 2147483648 * 10
        tau_q31 = struct.unpack('>1i', message_raw[14:18])[0]
        pid_tau = tau_q31 / 2147483648 * 10
        T_q31 = struct.unpack('>1i', message_raw[18:22])[0]
        pid_T = T_q31 / 2147483648 * 10
        if channel in self.parameters:
            pass
        else:
            self.parameters[channel] = dict()
        self.parameters[channel]["P"] = pid_p
        self.parameters[channel]["I"] = pid_i
        self.parameters[channel]["D"] = pid_d
        self.parameters[channel]["tau"] = pid_tau
        self.parameters[channel]["T"] = pid_T
        self.parameters_updated_from_device = True

    def read_status(self, channel: int, blocking=True):
        self.stream_command(USB_COMMAND_REPORT_STATUS + [channel])
        if blocking:
            while not self.new_status_available:
                time.sleep(0.01)
            self.new_status_available = False

    def read_parameters(self, channel: int, blocking=True):
        self.stream_command(USB_COMMAND_REPORT_PARAMETERS + [channel])
        if blocking:
            while not self.parameters_updated_from_device:
                time.sleep(0.01)
            self.parameters_updated_from_device = False

    def set_target(self, channel: int, target: int):
        self.stream_command(USB_COMMAND_SET_TARGET +
                            [channel] + [*struct.pack('>1i', target)])

    def set_pid_parameters(self, channel: int, pid_p: float, pid_i: float, pid_d: float):
        p = int(pid_p * 0.1 * 2147483648.0)
        i = int(pid_i * 0.1 * 2147483648.0)
        d = int(pid_d * 0.1 * 2147483648.0)
        self.stream_command(
            USB_COMMAND_SET_PID_PARAMETERS
            + [channel]
            + [*struct.pack('>1i', p)]
            + [*struct.pack('>1i', i)]
            + [*struct.pack('>1i', d)]
        )

    def set_working_mode(self, channel: int, working_mode: int):
        self.stream_command(USB_COMMAND_SET_WORKING_MODE + [channel] + [working_mode])
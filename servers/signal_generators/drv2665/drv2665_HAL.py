"""
USB Protocol defined for Firmware-STM32G431-DRV2665

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


def BIT(i):
    return (1 << i)


# /* Status Register */
DRV2665_FIFO_FULL = BIT(0)
DRV2665_FIFO_EMPTY = BIT(1)
DRV2665_FIFO_MASK = 0b00000011

# /* Control 1 Register */
DRV2660_CHIPID = 0b00000000
DRV2665_CHIPID = 0b00101000
DRV2667_CHIPID = 0b00111000
DRV266X_CHIPID_MASK = 0b01111000

DRV2665_25_VPP_GAIN = 0b00000000
DRV2665_50_VPP_GAIN = 0b00000001
DRV2665_75_VPP_GAIN = 0b00000010
DRV2665_100_VPP_GAIN = 0b00000011
DRV2665_GAIN_BITS_MASK = 0b00000011

DRV2665_DIGITAL_IN = 0b00000000
DRV2665_ANALOG_IN = 0b00000100
DRV2665_INPUT_MASK = 0b00000100

# /* Control 2 Register */
DRV2665_BOOST_EN = BIT(1)
DRV2665_STANDBY = BIT(6)
DRV2665_DEV_RST = BIT(7)
DRV2665_5_MS_IDLE_TOUT = 0b00000000
DRV2665_10_MS_IDLE_TOUT = 0b00000100
DRV2665_15_MS_IDLE_TOUT = 0b00001000
DRV2665_20_MS_IDLE_TOUT = 0b00001100
DRV2665_IDEL_TOUT_MASK = 0b00001100


USB_COMMAND_HEADER = [0x01, 0x01, 0x04, 0x05, 0x01, 0x04]
USB_COMMAND_TAIL = [0x01, 0x09, 0x01, 0x09, 0x08, 0x01, 0x00]
# USB commands
USB_COMMAND_SET_BUFFER = [0x01]
USB_COMMAND_READ_STATUS = [0x02]
USB_COMMAND_SET_GAIN = [0x03]
USB_COMMAND_SET_INPUT = [0x04]
USB_COMMAND_OVERRIDE_ENABLE = [0x05]
USB_COMMAND_USE_DEVICE_LOGIC_ENABLE = [0x06]
USB_COMMAND_SET_TIMEOUT = [0x07]
USB_COMMAND_ACTIVATE = [0x08]
USB_COMMAND_STANDBY = [0x09]
USB_COMMAND_RESET = [0x10]
USB_COMMAND_READ_CHIP_ID = [0x11]
# USB Protocol Enumerates for send
USBP_GAIN_25VPP = [0x00]
USBP_GAIN_50VPP = [0x01]
USBP_GAIN_75VPP = [0x02]
USBP_GAIN_100VPP = [0x03]
USBP_INPUT_DIGITAL = [0x00]
USBP_INPUT_ANALOG = [0x01]
USBP_TIMEOUT_5MS = [0x00]
USBP_TIMEOUT_10MS = [0x01]
USBP_TIMEOUT_15MS = [0x02]
USBP_TIMEOUT_20MS = [0x03]
# USB Protocol Enumerates for receive
USBP_CHIPID_DRV2660 = 0x00
USBP_CHIPID_DRV2665 = 0x05
USBP_CHIPID_DRV2667 = 0x07
USBP_CHIPID_UNKNOWN = 0xFF
# Header to identify report type
USB_REPORT_OK = 0x00
USB_REPORT_ERROR = 0x01
USB_REPORT_STATUS = 0x02
USB_REPORT_CHIPID = 0x03
# Standard Library
# 3-rd Party Library


def parse_message(message: bytes, status: dict = dict()) -> dict:
    """
    Parse report according to protocol, raises ValueError if
    a match is not found 
    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    msg_len = len(message)
    message = struct.unpack('{}B'.format(msg_len), message)
    report_type = message[0]
    if report_type == USB_REPORT_OK:
        print("Device reported OK")
    elif report_type == USB_REPORT_ERROR:
        if len(message) == 1:
            print("Device reported ERROR.")
        else:
            print("Device reported ERROR, reason: ", message[1:])
    elif report_type == USB_REPORT_STATUS:
        if len(message) == 4:
            print("Status Report: ", message[1:])
            print(parse_status(*message[1:], status=status))
        else:
            raise ValueError("Corrupted status report message.")
    elif report_type == USB_REPORT_CHIPID:
        if len(message) == 2:
            print("Chip ID: ", message[1])
            print(parse_chip_id(message[1], status=status))
        else:
            raise ValueError("Corrupted chip ID message.")
    else:
        raise ValueError("Not supported report type.")

    return status


def parse_chip_id(chipid: int, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_CHIPID messages.

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    if chipid == USBP_CHIPID_DRV2660:
        status["ChipID"] = "DRV2660"
    elif chipid == USBP_CHIPID_DRV2665:
        status["ChipID"] = "DRV2665"
    elif chipid == USBP_CHIPID_DRV2667:
        status["ChipID"] = "DRV2667"
    else:
        status["ChipID"] = "UNKNOWN"

    return status


def parse_status(fifo: int, ctrl1: int, ctrl2: int, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_STATUS messages

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    # ================= FIFO =================
    fifo_is_full = bool(fifo & DRV2665_FIFO_FULL)
    fifo_is_empty = bool(fifo & DRV2665_FIFO_EMPTY)
    if ((not fifo_is_full) and (not fifo_is_empty)):
        status["FIFO"] = "NotEmptyAndNotFull"
    elif ((not fifo_is_full) and fifo_is_empty):
        status["FIFO"] = "Empty"
    elif (fifo_is_full and (not fifo_is_empty)):
        status["FIFO"] = "Full"
    elif (fifo_is_full and fifo_is_empty):
        status["FIFO"] = "Error"
    else:
        raise ValueError("Unknown FIFO Status")
    # ================= CTRL1 =================
    # Chip ID
    chipid_bits = ctrl1 & DRV266X_CHIPID_MASK
    if (not (chipid_bits ^ DRV2660_CHIPID)):
        status["ChipID"] = "DRV2660"
    elif (not (chipid_bits ^ DRV2665_CHIPID)):
        status["ChipID"] = "DRV2665"
    elif (not (chipid_bits ^ DRV2667_CHIPID)):
        status["ChipID"] = "DRV2667"
    else:
        raise ValueError("Unknown Chip ID")
    # Gain
    gain_bits = ctrl1 & DRV2665_GAIN_BITS_MASK
    if (not (gain_bits ^ DRV2665_25_VPP_GAIN)):
        status["Gain"] = "25Vpp"
    elif (not (gain_bits ^ DRV2665_50_VPP_GAIN)):
        status["Gain"] = "50Vpp"
    elif (not (gain_bits ^ DRV2665_75_VPP_GAIN)):
        status["Gain"] = "75Vpp"
    elif (not (gain_bits ^ DRV2665_100_VPP_GAIN)):
        status["Gain"] = "100Vpp"
    else:
        raise ValueError("Unknown Gain Option")
    # Input Type
    input_type_bit = ctrl1 & DRV2665_INPUT_MASK
    if input_type_bit & DRV2665_ANALOG_IN:
        status["Input"] = "Analog"
    else:
        status["Input"] = "Digital"
    # ================= CTRL2 =================
    # Override Enable
    if ctrl2 & DRV2665_BOOST_EN:
        status["OverrideEnable"] = True
    else:
        status["OverrideEnable"] = False
    # Standby
    if ctrl2 & DRV2665_STANDBY:
        status["Standby"] = True
    else:
        status["Standby"] = False
    # Reset
    if ctrl2 & DRV2665_DEV_RST:
        status["Reset"] = True
    else:
        status["Reset"] = False
    # Timeout
    timeout_bits = ctrl2 & DRV2665_IDEL_TOUT_MASK
    if (not (timeout_bits ^ DRV2665_5_MS_IDLE_TOUT)):
        status["Timeout"] = "5ms"
    elif (not (timeout_bits ^ DRV2665_10_MS_IDLE_TOUT)):
        status["Timeout"] = "10ms"
    elif (not (timeout_bits ^ DRV2665_15_MS_IDLE_TOUT)):
        status["Timeout"] = "15ms"
    elif (not (timeout_bits ^ DRV2665_20_MS_IDLE_TOUT)):
        status["Timeout"] = "20ms"
    else:
        raise ValueError("Unknown Timeout Option")

    return status


class DRV2665:
    def __init__(self, com='COM4') -> None:
        self.com = com
        self.commands_buffer = list()
        self.messages_from_device_buffer = list()
        self.serial_manager_thread_running = True
        self.serial_manager_thread = Thread(target=self.serial_task)
        self.serial_manager_thread.start()
        self.message_handler_thread_running = True
        self.message_handler_thread = Thread(target=self.message_handler_task)
        self.message_handler_thread.start()
        self.status = {}

    def shutdown(self):
        self.serial_manager_thread_running = False
        self.message_handler_thread_running = False

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
                    parse_message(earliest_message, status=self.status)
                except ValueError:
                    print("Error parsing message.")

    def stream_command(self, command: list[int]):
        command_length = len(command)
        assert command_length < 65536, "Command length must be within 0 - 65535"
        to_send = USB_COMMAND_HEADER + \
            [(command_length >> 8) % 256, command_length % 256] + \
            command + USB_COMMAND_TAIL
        bytes_length = len(to_send)
        to_send = struct.pack('{}B'.format(bytes_length), *to_send)
        self.commands_buffer.append(to_send)

    def update_buffer(self, new_buffer: list[int]):
        """
        Update on-board waveform buffer
            command: 0x01
            content: new buffer to be copied to waveform buffer
            return: 1 byte, status
        """
        self.stream_command(USB_COMMAND_SET_BUFFER + new_buffer)

    def read_status(self):
        """
        Request to report all current status and configuration
            command: 0x02
            content: none
            return: 3 bytes, representing FIFO, CTRL1, CTRL2
        """
        self.stream_command(USB_COMMAND_READ_STATUS)

    def set_gain(self, gain_option: str):
        """
        Set gain
            command: 0x03
            content: one of GAIN enums
            return: 1 byte, status
        """
        if gain_option == "25Vpp":
            gain = USBP_GAIN_25VPP
        elif gain_option == "50Vpp":
            gain = USBP_GAIN_50VPP
        elif gain_option == "75Vpp":
            gain = USBP_GAIN_75VPP
        elif gain_option == "100Vpp":
            gain = USBP_GAIN_100VPP
        else:
            raise ValueError(
                "Gain option {} not available in this device".format(gain_option))
        self.stream_command(USB_COMMAND_SET_GAIN + gain)

    def set_input_type(self, input_type: str):
        """
        Set input type
            command: 0x04
            content: one of INPUT enums
            return: 1byte, status
        """
        if input_type == "Analog":
            i = USBP_INPUT_ANALOG
        elif input_type == "Digital":
            i = USBP_INPUT_DIGITAL
        else:
            raise ValueError(
                "Input type {} is not supported in this device".format(input_type))
        self.stream_command(USB_COMMAND_SET_INPUT + i)

    def override_enable(self):
        """
        Override enable logic in chip, enable boost converter and amplifier indefinitely, 
        ignoring idle timeouts.
            command: 0x05
            content: none
            return: 1byte, status
        """
        self.stream_command(USB_COMMAND_OVERRIDE_ENABLE)

    def use_device_logic_enable(self):
        """
        Opposite to override_enable, use device logic to control boost converter 
        and amplifier enables.
            command: 0x06
            content: none
            return: 1byte, status
        """
        self.stream_command(USB_COMMAND_USE_DEVICE_LOGIC_ENABLE)

    def set_timeout(self, timeout_option: str):
        """
        Set idle timeout for chip when FIFO is empty
            command: 0x07
            content: one of TIMEOUT enums
            return: 1 byte, status
        """
        if timeout_option == "5ms":
            tout = USBP_TIMEOUT_5MS
        elif timeout_option == "10ms":
            tout = USBP_TIMEOUT_10MS
        elif timeout_option == "15ms":
            tout = USBP_TIMEOUT_15MS
        elif timeout_option == "20ms":
            tout = USBP_TIMEOUT_20MS
        else:
            raise ValueError(
                "Timeout option {} not available in this device".format(timeout_option))
        self.stream_command(USB_COMMAND_SET_TIMEOUT + tout)

    def activate(self):
        """
        Wake up the device from standby mode
            command: 0x08
            content: none
            return: 1byte, status
        """
        self.stream_command(USB_COMMAND_ACTIVATE)

    def standby(self):
        """
        Put the device to low power standby mode
            command: 0x09
            content: none
            return: 1byte, status
        """
        self.stream_command(USB_COMMAND_STANDBY)

    def reset(self):
        """
        Reset the device, all options go to default values
            command: 0x10
            content: none
            return: 1byte, status
        """
        self.stream_command(USB_COMMAND_RESET)

    def read_chip_id(self):
        """
        Read the chip ID
            command: 0x11
            content: none
            return: 1byte, status, followed by 2 bytes, chipid report.
        """
        self.stream_command(USB_COMMAND_READ_CHIP_ID)

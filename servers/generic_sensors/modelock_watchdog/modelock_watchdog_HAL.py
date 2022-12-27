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


USB_COMMAND_HEADER = [0x01, 0x01, 0x04, 0x05, 0x01, 0x04]
USB_COMMAND_TAIL = [0x01, 0x09, 0x01, 0x09, 0x08, 0x01, 0x00]
# USB commands
USB_COMMAND_READ_TEMPERATURE = [0x01]
USB_COMMAND_READ_HUMIDITY = [0x02]
USB_COMMAND_PROBE = [0x03]
USB_COMMAND_GET_STATUS = [0x04]
USB_COMMAND_CLEAR_STATUS = [0x05]
USB_COMMAND_SET_POWER_MODE = [0x06]
USB_COMMAND_READ_SERIAL = [0x07]
USB_COMMAND_SET_TEMPERATURE_ALERT_THRESHOLD_LOW = [0x08]
USB_COMMAND_SET_HUMIDITY_ALERT_THRESHOLD_LOW = [0x09]
USB_COMMAND_SET_TEMPERATURE_ALERT_THRESHOLD_HIGH = [0x0a]
USB_COMMAND_SET_HUMIDITY_ALERT_THRESHOLD_HIGH = [0x0b]
USB_COMMAND_READ_FREQUENCY = [0x0c]
USB_COMMAND_START_CONTINUOUS_READ = [0x0d]
USB_COMMAND_STOP_CONTINUOUS_READ = [0x0e]
USB_COMMAND_READ_ALL = [0x0f]
USB_COMMAND_SET_COMPARATOR_THRESHOLD = [0x10]
# Enumerates

# Header to identify report type
USB_REPORT_OK = 0x00
USB_REPORT_ERROR = 0x01
USB_REPORT_TEMPERATURE_DATA = 0x02
USB_REPORT_HUMIDITY_DATA = 0x03
USB_REPORT_FREQUENCY_DATA = 0x04
USB_REPORT_COUNTER_DATA = 0x05
USB_REPORT_ADC_DATA = 0x06
USB_REPORT_ALERT = 0x07
USB_REPORT_CHIPID = 0x08
# Standard Library
# 3-rd Party Library


def parse_message(message_raw: bytes, status: dict = dict()) -> dict:
    """
    Parse report according to protocol, raises ValueError if
    a match is not found 
    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    msg_len = len(message_raw)
    message = struct.unpack('{}B'.format(msg_len), message_raw)
    report_type = message[0]
    if report_type == USB_REPORT_OK:
        print("Device reported OK")
    elif report_type == USB_REPORT_ERROR:
        if len(message) == 1:
            print("Device reported ERROR.")
        else:
            print("Device reported ERROR, reason: ", message[1:])
    elif report_type == USB_REPORT_TEMPERATURE_DATA:
        if len(message) == 9:
            # print("Temperature Report: ", message[1:])
            parse_status_temperature(message[1:], status=status)
        elif len(message) > 9:
            # several reports are stick together because USB stream has no real package
            parse_message(message_raw[0:9], status=status)
            parse_message(message_raw[9:], status=status)
        else:
            print("Corrupted: ", message)
            raise ValueError("Corrupted temperature status report message.")
    elif report_type == USB_REPORT_HUMIDITY_DATA:
        if len(message) == 9:
            # print("Humidity Report: ", message[1:])
            parse_status_humidity(message[1:], status=status)
        elif len(message) > 9:
            # several reports are stick together because USB stream has no real package
            parse_message(message_raw[0:9], status=status)
            parse_message(message_raw[9:], status=status)
        else:
            raise ValueError("Corrupted humidity status report message.")
    elif report_type == USB_REPORT_FREQUENCY_DATA:
        if len(message) == 5:
            # print("Frequency Report: ", message[1:])
            parse_status_frequency(message[1:], status=status)
        elif len(message) > 5:
            # several reports are stick together because USB stream has no real package
            parse_message(message_raw[0:5], status=status)
            parse_message(message_raw[5:], status=status)
        else:
            raise ValueError("Corrupted frequency status report message.")
    elif report_type == USB_REPORT_COUNTER_DATA:
        if len(message) == 5:
            # print("Counter Report: ", message[1:])
            parse_status_counter(message[1:], status=status)
        elif len(message) > 5:
            # several reports are stick together because USB stream has no real package
            parse_message(message_raw[0:5], status=status)
            parse_message(message_raw[5:], status=status)
        else:
            raise ValueError("Corrupted counter status report message.")
    elif report_type == USB_REPORT_CHIPID:
        if len(message) == 2:
            print("Chip ID: ", message[1])
            print(parse_chip_id(message[1], status=status))
        else:
            raise ValueError("Corrupted chip ID message.")
    else:
        raise ValueError("Not supported report type.")
    # print(status)
    return status


def parse_chip_id(chipid: int, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_CHIPID messages.

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    status["ChipID"] = chipid

    return status


def parse_status_temperature(temperature_data, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_TEMPERATURE_DATA messages

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    assert len(temperature_data) == 8, "Corrupted data"
    sensor_1 = temperature_data[0:4]
    sensor_2 = temperature_data[4:8]
    status["Temperature1"] = (
        sensor_1[0] << 24) + (sensor_1[1] << 16) + (sensor_1[2] << 8) + sensor_1[3]
    status["Temperature2"] = (
        sensor_2[0] << 24) + (sensor_2[1] << 16) + (sensor_2[2] << 8) + sensor_2[3]
    return status


def parse_status_humidity(humidity_data, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_HUMIDITY_DATA messages

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    assert len(humidity_data) == 8, "Corrupted data"
    sensor_1 = humidity_data[0:4]
    sensor_2 = humidity_data[4:8]
    status["Humidity1"] = (sensor_1[0] << 24) + \
        (sensor_1[1] << 16) + (sensor_1[2] << 8) + sensor_1[3]
    status["Humidity2"] = (sensor_2[0] << 24) + \
        (sensor_2[1] << 16) + (sensor_2[2] << 8) + sensor_2[3]
    return status


def parse_status_frequency(frequency_data, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_FREQUENCY_DATA messages

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    assert len(frequency_data) == 4, "Corrupted data"
    status["Frequency"] = (frequency_data[0] << 24) + (frequency_data[1]
                                                       << 16) + (frequency_data[2] << 8) + frequency_data[3]
    return status


def parse_status_counter(counter_data, status: dict = dict()) -> dict:
    """
    Parse USB_REPORT_COUNTER_DATA messages.

    If given a status dict, the function updates values in
    the dict, if not, the function creates and returns a new 
    status dict to hold parsed results.
    """
    assert len(counter_data) == 4, "Corrupted Counter Data"
    status["Counter"] = (counter_data[0] << 24) + (counter_data[1]
                                                   << 16) + (counter_data[2] << 8) + counter_data[3]
    status["Timestamp"] = time.time()
    return status


class ModelockWatchdog:
    def __init__(self, com='COM5') -> None:
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
        self.new_data_available = False

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

    def read_temperature(self):
        """
        Retrive on-board buffered temperature data
            command: 0x01
            content: none
            return: 9 bytes, 1 byte header, 4 bytes sensor 1 temperature, 4 bytes sensor 2 temperature
        """
        self.stream_command(USB_COMMAND_READ_TEMPERATURE)

    def read_humidity(self):
        """
        Retrive on-board buffered humidity data
            command: 0x02
            content: none
            return: 9 bytes, 1 byte header, 4 bytes sensor 1 humidity, 4 bytes sensor 2 humidity
        """
        self.stream_command(USB_COMMAND_READ_HUMIDITY)

    def read_frequency(self):
        """
        Retrive on-board buffered frequency data
            command: 0x0c
            content: none
            return: 5 bytes, 1 byte header, 4 bytes frequency data
        """
        self.stream_command(USB_COMMAND_READ_HUMIDITY)

    def start_continuous_read(self):
        """
        Start continuous measurement mode, the board continuously measures data and transmits all
        available data to computer
            command: 0x0d
            content: none
            return: 1 byte OK/ERROR, then messages of data report type, continuously
        """
        self.stream_command(USB_COMMAND_START_CONTINUOUS_READ)

    def stop_continuous_read(self):
        """
        Stop continuous measurement mode.
            command: 0x0e
            content: none
            return: 1 byte OK/ERROR
        """
        self.stream_command(USB_COMMAND_STOP_CONTINUOUS_READ)
    
    def set_comparator_threshold(self, new_threshold:int):
        pass

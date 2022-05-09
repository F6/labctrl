#!/usr/bin/python3
"""
Simple GCode streaming script
"""
import time 
import serial
 
port = 'COM1'
file = 'spiral.gcode'
 
def remove_comment(string):
    """Remove comments from GCode if any"""
    if string.find(';') == -1:
        return string
    return string[:string.index(';')]
 

print('Opening Serial Port')
SERIAL_CONNECTION = serial.Serial(port, 115200, timeout=1)


with open(file, 'r') as f:
    print('Opening GCode File')
    GCODE_FILE = f.readlines()
 
# Hit enter a few times to wake up
SERIAL_CONNECTION.write(str.encode("\r\n\r\n"))
time.sleep(2)  # Wait for initialization
SERIAL_CONNECTION.flushInput()  # Flush startup text in serial input
print('Sending GCode')

# Stream g-code

SERIAL_CONNECTION.write('G1 F1000\n'.encode())
 
while True:
    for line in GCODE_FILE:
        cmd_gcode = remove_comment(line)
        cmd_gcode = cmd_gcode.strip()  # Strip all EOL characters for streaming
        if (cmd_gcode.isspace() is False and len(cmd_gcode) > 0):
            print('Sending: ' + cmd_gcode)
            SERIAL_CONNECTION.write(cmd_gcode.encode() +
                                    str.encode('\n'))  # Send g-code block
            # Wait for response with carriage return
            grbl_out = SERIAL_CONNECTION.readline()
            print(grbl_out.strip().decode("utf-8"))


SERIAL_CONNECTION.close()
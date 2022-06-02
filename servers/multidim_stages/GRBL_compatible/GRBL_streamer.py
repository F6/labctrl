import serial

class GRBL:
    def __init__(self) -> None:
        self.com = 'COM5'
        self.ser = serial.Serial(self.com, baudrate=115200, timeout=1)
    
    def send_gcode(self, gcode:str):
        gcode = gcode + '\n'
        self.ser.write(gcode.encode())
        return self.ser.readline().decode()
    
    def blocking_g1_command(self, gcode:str):
        # sanity check
        assert gcode.startswith('G1')
        res = self.send_gcode(gcode)
        if res.startswith('ok'):
            self.ser.write('G4 P0\n'.encode()) # G4 is wait in seconds, G4 P0 is block until current movement finish. This only applies to GRBL.
            res = self.ser.readline().decode()
        return res

grbl = GRBL()
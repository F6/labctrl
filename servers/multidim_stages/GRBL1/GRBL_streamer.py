import serial
import time

class GRBL:
    def __init__(self, com:str) -> None:
        self.com = com
        self.ser = serial.Serial(self.com, baudrate=115200, timeout=30)
    
    def send_gcode(self, gcode:str):
        gcode = gcode + '\n'
        self.ser.write(gcode.encode())
        res = self.ser.readline()
        s = res.decode()
        while self.ser.in_waiting:
            res = self.ser.readline()
            s += res.decode()
        return s
        
    def parse_status(self, s):
        try:
            # print(s)
            # sys.stdout.flush()
            s = s.split('\r\n')
            s1 = ''
            for i in s:
                if i.startswith("<"):
                    s1 = i
                    break
            s1 = s1.strip()
            s2 = s1[1:-1]
            s3 = s2.split('|')
            d = dict()
            d["status"] = s3[0]
            pos = s3[1]
            pos = pos[5:]
            pos = pos.split(',')
            pos = list(map(float, pos))
            d["pos"] = pos
            return d
        except Exception as e:
            print(s)
            raise Exception

    
    def blocking_g1_command(self, gcode:str):
        # sanity check
        # assert gcode.startswith('G1')
        res = self.send_gcode(gcode)
        while True:
            time.sleep(0.05)
            res = self.parse_status(self.send_gcode("?"))
            if res["status"] == 'Idle':
                break
        return res


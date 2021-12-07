
import socket

EOS_CHAR = '\n'   # END OF STRING
ACK_CHAR = '%'    # SUCCESS
NAK_CHAR = '!'    # INVALID COMMAND
FAULT_CHAR = '#'  # ERROR EXECUTING
TIMEOUT_CHAR = '$'

class Ensemble:
    def __init__(self, ip:str, port:int) -> None:
        self._ip = ip
        self._port = port

    def send_command(self, cmd:str):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
            sock.connect((self._ip, self._port))
            sock.send(cmd.encode())
            buf = sock.recv(4096)
            sock.close()
            return buf
        except ConnectionRefusedError:
            print("Connection Refused")
        
    def enable(self):
        return self.send_command("ENABLE X\n")
    
    def moveabs(self, pos:float):
        cmd = "MOVEABS X{pos:.6f} XF10.0\n".format(pos=pos)
        # print(cmd)
        return self.send_command(cmd)

    def autohome(self):
        return self.moveabs(0.000000)

    def getpos(self):
        return self.send_command("PFBK X\n")

ip = '192.168.8.6'
port = 8000

ensemble = Ensemble(ip, port)
# we do not disable it...
ensemble.enable()

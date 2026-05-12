import socket

class TelnetClient:
    def __init__(self, host, port=23):
        self.host = host
        self.port = port

    def handshake(self):
        s = socket.socket()
        s.settimeout(2)
        try:
            s.connect((self.host, self.port))
            banner = s.recv(1024)
        except:
            banner = b""
        return {"banner": banner.decode(errors="ignore"), "response": b""}

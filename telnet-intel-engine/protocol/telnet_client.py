import socket
import time

IAC = bytes([255])
DO = bytes([253])

OPT_ECHO = bytes([1])
OPT_SGA = bytes([3])
OPT_TTYPE = bytes([24])
OPT_LINEMODE = bytes([34])
OPT_OLD_ENVIRON = bytes([36])
OPT_NEW_ENVIRON = bytes([39])
OPT_STATUS = bytes([5])
OPT_NAWS = bytes([31])
OPT_BINARY = bytes([0])

class TelnetClient:
    def __init__(self, host, port=23, timeout=2):
        self.host = host
        self.port = port
        self.timeout = timeout

    def handshake(self):
        initial = b""
        response = b""
        banner_text = ""

        s = socket.socket()
        s.settimeout(self.timeout)

        try:
            s.connect((self.host, self.port))

            initial = self._recv(s)

            # Safe RFC-style option negotiation only.
            s.sendall(self._safe_negotiation())

            time.sleep(0.5)
            response = self._recv(s)

            combined = initial + response
            banner_text = combined.decode("latin1", errors="ignore")

        except Exception as e:
            banner_text = f"ERROR: {e}"

        finally:
            try:
                s.close()
            except Exception:
                pass

        return {
            "banner": banner_text,
            "initial": initial,
            "response": initial + response,
        }

    def _recv(self, sock, size=4096):
        try:
            return sock.recv(size)
        except Exception:
            return b""

    def _safe_negotiation(self):
        return (
            IAC + DO + OPT_ECHO +
            IAC + DO + OPT_SGA +
            IAC + DO + OPT_TTYPE +
            IAC + DO + OPT_LINEMODE +
            IAC + DO + OPT_OLD_ENVIRON +
            IAC + DO + OPT_NEW_ENVIRON +
            IAC + DO + OPT_STATUS +
            IAC + DO + OPT_NAWS +
            IAC + DO + OPT_BINARY
        )

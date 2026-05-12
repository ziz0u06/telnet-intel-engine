from stream.producer import TelnetProducer
from stream.topics import TELNET_JOBS

producer = TelnetProducer()

producer.send(TELNET_JOBS, {
    "target": "127.0.0.1"
})

print("[+] job sent")

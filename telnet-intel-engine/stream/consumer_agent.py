import json
from kafka import KafkaConsumer

from stream.producer import TelnetProducer
from stream.topics import TELNET_JOBS, TELNET_RAW
from scanner.worker import scan_host

consumer = KafkaConsumer(
    TELNET_JOBS,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = TelnetProducer()

print("[+] Agent consumer started")

for msg in consumer:
    job = msg.value
    target = job.get("target")

    if not target:
        continue

    print(f"[+] scanning {target}")

    result = scan_host(target)

    if result:
        producer.send(TELNET_RAW, result)
        print(f"[+] telemetry sent for {target}")

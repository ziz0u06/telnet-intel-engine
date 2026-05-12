import json
from kafka import KafkaProducer

class TelnetProducer:
    def __init__(self, bootstrap_servers="localhost:9092"):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send(self, topic, payload):
        self.producer.send(topic, payload)
        self.producer.flush()

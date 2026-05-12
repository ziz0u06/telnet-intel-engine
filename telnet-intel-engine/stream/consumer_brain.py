import json
from kafka import KafkaConsumer

from stream.producer import TelnetProducer
from stream.topics import TELNET_RAW, TELNET_FEATURES, TELNET_PREDICTIONS, TELNET_DATASET
from features.extractor import extract_features
from ml.bayesian import BayesianClassifier

producer = TelnetProducer()
model = BayesianClassifier()

consumer = KafkaConsumer(
    TELNET_RAW,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

def auto_label(prediction):
    p27 = prediction.get("2.7", 0.0)
    p28 = prediction.get("2.8", 0.0)

    if p28 >= 0.90:
        return "2.8", True

    if p27 >= 0.90:
        return "2.7", True

    return "unknown", False

print("[+] Brain consumer started")

for msg in consumer:
    raw_event = msg.value

    raw = {
        "banner": raw_event.get("banner", ""),
        "response": raw_event.get("response", b"")
    }

    features = extract_features(raw)
    prediction = model.predict(features)
    label, trusted = auto_label(prediction)

    feature_event = {
        "ip": raw_event.get("ip"),
        "features": features
    }

    prediction_event = {
        "ip": raw_event.get("ip"),
        "prediction": prediction,
        "label": label,
        "trusted": trusted
    }

    dataset_event = {
        "ip": raw_event.get("ip"),
        "banner": raw_event.get("banner", ""),
        "features": features,
        "prediction": prediction,
        "label": label,
        "trusted": trusted
    }

    producer.send(TELNET_FEATURES, feature_event)
    producer.send(TELNET_PREDICTIONS, prediction_event)
    producer.send(TELNET_DATASET, dataset_event)

    print(f"[+] processed {raw_event.get('ip')} label={label} trusted={trusted}")

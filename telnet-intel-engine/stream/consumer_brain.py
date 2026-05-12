import json
from kafka import KafkaConsumer

from stream.producer import TelnetProducer
from stream.topics import (
    TELNET_RAW,
    TELNET_FEATURES,
    TELNET_PREDICTIONS,
    TELNET_DATASET,
)

from features.extractor import extract_features
from features.vectorizer import vectorize

from ml.bayesian import BayesianClassifier
from ml.anomaly import anomaly_score

from db.store import append_dataset

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

    vector = vectorize(features)

    prediction = model.predict(features)

    anomaly = anomaly_score(features)

    label, trusted = auto_label(prediction)

    feature_event = {
        "ip": raw_event.get("ip"),
        "features": features,
        "vector": vector,
        "iac_order": features.get("iac_order"),
        "iac_event_count": features.get("iac_event_count"),
    }

    prediction_event = {
        "ip": raw_event.get("ip"),
        "prediction": prediction,
        "top_class": max(prediction, key=prediction.get),
        "confidence": max(prediction.values()),
        "label": label,
        "trusted": trusted,
        "anomaly": anomaly,
    }

    dataset_event = {
        "ip": raw_event.get("ip"),
        "banner": raw_event.get("banner", ""),
        "features": features,
        "vector": vector,
        "prediction": prediction,
        "top_class": max(prediction, key=prediction.get),
        "confidence": max(prediction.values()),
        "label": label,
        "trusted": trusted,
        "anomaly": anomaly,
    }

    producer.send(TELNET_FEATURES, feature_event)

    producer.send(TELNET_PREDICTIONS, prediction_event)

    producer.send(TELNET_DATASET, dataset_event)

    append_dataset(dataset_event)

    print(
        f"[+] processed "
        f"{raw_event.get('ip')} "
        f"label={label} "
        f"trusted={trusted} "
        f"anomaly={anomaly['score']}"
    )

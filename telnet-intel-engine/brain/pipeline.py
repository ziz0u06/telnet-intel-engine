from bus.consumer import consume
from bus.producer import publish


def process():
    events = consume("telnet.raw")

    for event in events:
        prediction = {
            "job_id": event["job_id"],
            "label": "simulated_version",
            "confidence": event["payload"]["confidence"],
            "trusted": event["payload"]["confidence"] > 0.85,
        }

        publish("telnet.predictions", prediction)


if __name__ == "__main__":
    process()
    print("Pipeline processing complete.")
import json
from pathlib import Path

QUEUE_DIR = Path("queue")
QUEUE_DIR.mkdir(exist_ok=True)


def publish(topic: str, message: dict) -> None:
    topic_file = QUEUE_DIR / f"{topic}.jsonl"
    with open(topic_file, "a") as f:
        f.write(json.dumps(message) + "\n")
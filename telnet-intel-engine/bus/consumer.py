import json
from pathlib import Path


def consume(topic: str):
    topic_file = Path("queue") / f"{topic}.jsonl"

    if not topic_file.exists():
        return []

    events = []
    with open(topic_file) as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    return events
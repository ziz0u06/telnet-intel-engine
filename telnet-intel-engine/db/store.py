import json
from pathlib import Path

DATASET_PATH = Path("queue/telnet.dataset.jsonl")

def append_dataset(event):

    DATASET_PATH.parent.mkdir(exist_ok=True)

    with open(DATASET_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

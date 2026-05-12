import time
from bus.producer import publish


def collect(job: dict) -> dict:
    return {
        "job_id": job.get("job_id"),
        "source": "agent-local",
        "timestamp": time.time(),
        "status": "ok",
        "payload": {
            "banner": "Simulated Telnet Banner",
            "confidence": 0.87,
        },
    }


def run(job: dict) -> None:
    event = collect(job)
    publish("telnet.raw", event)


if __name__ == "__main__":
    sample_job = {
        "job_id": "demo-001",
        "target": "example-target"
    }
    run(sample_job)
    print("Agent event published.")
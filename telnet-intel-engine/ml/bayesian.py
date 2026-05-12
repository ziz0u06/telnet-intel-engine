import math

class BayesianClassifier:

    def __init__(self):
        self.classes = ["2.7", "2.8", "vendor", "embedded", "unknown"]

    def predict(self, features):

        scores = {
            "2.7": math.log(0.20),
            "2.8": math.log(0.25),
            "vendor": math.log(0.25),
            "embedded": math.log(0.15),
            "unknown": math.log(0.15),
        }

        def add(cls, value):
            scores[cls] += value

        # banner signals
        if features.get("banner_inetutils"):
            add("2.7", 1.2)
            add("2.8", 1.2)

        if features.get("banner_telnetd"):
            add("2.7", 0.7)
            add("2.8", 0.7)

        if features.get("banner_busybox"):
            add("embedded", 2.5)

        if features.get("banner_cisco_like"):
            add("vendor", 2.5)

        # behavioral signals
        if features.get("linemode"):
            add("2.7", 0.8)
            add("2.8", 1.0)

        if features.get("new_environ"):
            add("2.7", 0.8)
            add("2.8", 0.8)

        if features.get("status"):
            add("2.7", 0.4)
            add("2.8", 0.4)

        if features.get("ttype"):
            add("2.7", 0.3)
            add("2.8", 0.3)
            add("vendor", 0.2)

        if (
            features.get("binary")
            and features.get("naws")
            and features.get("sga")
        ):
            add("vendor", 0.9)

        event_count = features.get("iac_event_count", 0)

        if event_count >= 8:
            add("2.7", 0.5)
            add("2.8", 0.6)

        elif event_count == 0:
            add("unknown", 1.0)

        # lightweight 2.8 tilt
        if (
            features.get("linemode")
            and features.get("new_environ")
            and features.get("status")
            and not features.get("banner_busybox")
            and not features.get("banner_cisco_like")
        ):
            add("2.8", 0.5)

        return self._softmax(scores)

    def _softmax(self, log_scores):

        max_score = max(log_scores.values())

        exps = {
            k: math.exp(v - max_score)
            for k, v in log_scores.items()
        }

        total = sum(exps.values())

        return {
            k: round(v / total, 6)
            for k, v in exps.items()
        }

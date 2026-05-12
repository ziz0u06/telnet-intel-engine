def anomaly_score(features):
    score = 0.0
    reasons = []

    if features.get("iac_event_count", 0) == 0:
        score += 0.4
        reasons.append("no_iac_events")

    if features.get("iac_event_count", 0) > 20:
        score += 0.3
        reasons.append("high_iac_event_count")

    if features.get("banner_inetutils") and features.get("banner_cisco_like"):
        score += 0.5
        reasons.append("conflicting_banner_signals")

    if not any([
        features.get("banner_inetutils"),
        features.get("banner_telnetd"),
        features.get("banner_busybox"),
        features.get("banner_cisco_like"),
        features.get("linemode"),
        features.get("ttype"),
        features.get("new_environ"),
        features.get("status"),
        features.get("naws"),
    ]):
        score += 0.3
        reasons.append("low_signal")

    score = min(score, 1.0)

    return {
        "score": round(score, 4),
        "is_anomaly": score >= 0.6,
        "reasons": reasons,
    }

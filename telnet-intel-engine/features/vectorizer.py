FEATURE_KEYS = [
    "linemode",
    "ttype",
    "new_environ",
    "status",
    "naws",
    "binary",
    "echo",
    "sga",
    "banner_inetutils",
    "banner_telnetd",
    "banner_busybox",
    "banner_cisco_like",
    "iac_count",
    "iac_event_count",
]

def vectorize(features):
    vector = []

    for key in FEATURE_KEYS:
        value = features.get(key, False)

        if isinstance(value, bool):
            vector.append(1 if value else 0)
        elif isinstance(value, int):
            vector.append(value)
        elif isinstance(value, float):
            vector.append(value)
        else:
            vector.append(0)

    return vector

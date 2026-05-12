from protocol.iac_parser import parse_iac, summarize_iac

def extract_features(raw):
    banner = raw.get("banner", "").lower()
    response = raw.get("response", b"")

    if isinstance(response, str):
        response = response.encode("latin1", errors="ignore")

    events = parse_iac(response)
    summary = summarize_iac(events)

    return {
        "banner_inetutils": "inetutils" in banner,
        "banner_telnetd": "telnetd" in banner,
        "banner_busybox": "busybox" in banner,
        "banner_cisco_like": "user access verification" in banner,

        "linemode": summary["linemode"],
        "ttype": summary["ttype"],
        "new_environ": summary["new_environ"],
        "status": summary["status"],
        "naws": summary["naws"],
        "binary": summary["binary"],
        "echo": summary["echo"],
        "sga": summary["sga"],

        "iac_count": response.count(bytes([255])),
        "iac_event_count": summary["iac_event_count"],
        "iac_order": summary["iac_order"],
    }

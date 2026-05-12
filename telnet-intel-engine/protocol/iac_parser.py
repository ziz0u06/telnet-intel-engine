IAC = 255

COMMANDS = {
    240: "SE",
    250: "SB",
    251: "WILL",
    252: "WONT",
    253: "DO",
    254: "DONT",
}

OPTIONS = {
    0: "BINARY",
    1: "ECHO",
    3: "SUPPRESS_GO_AHEAD",
    5: "STATUS",
    24: "TTYPE",
    31: "NAWS",
    34: "LINEMODE",
    36: "OLD_ENVIRON",
    39: "NEW_ENVIRON",
}

def parse_iac(data: bytes):
    events = []
    i = 0

    while i < len(data):
        if data[i] != IAC:
            i += 1
            continue

        if i + 1 >= len(data):
            break

        cmd = data[i + 1]

        if cmd in (251, 252, 253, 254):
            if i + 2 < len(data):
                opt = data[i + 2]
                events.append({
                    "cmd": COMMANDS.get(cmd, f"CMD_{cmd}"),
                    "option": OPTIONS.get(opt, f"OPT_{opt}"),
                    "option_code": opt,
                })
                i += 3
                continue

        if cmd == 250:
            # subnegotiation: IAC SB ... IAC SE
            start = i + 2
            end = data.find(bytes([IAC, 240]), start)
            if end == -1:
                break

            payload = data[start:end]
            opt = payload[0] if payload else None

            events.append({
                "cmd": "SB",
                "option": OPTIONS.get(opt, f"OPT_{opt}") if opt is not None else "UNKNOWN",
                "option_code": opt,
                "payload_len": len(payload),
            })

            i = end + 2
            continue

        events.append({
            "cmd": COMMANDS.get(cmd, f"CMD_{cmd}"),
            "option": None,
            "option_code": None,
        })

        i += 2

    return events

def summarize_iac(events):
    supported = {
        "linemode": False,
        "ttype": False,
        "new_environ": False,
        "status": False,
        "naws": False,
        "binary": False,
        "echo": False,
        "sga": False,
    }

    order = []

    for e in events:
        opt = e.get("option")
        if opt:
            order.append(f"{e.get('cmd')}:{opt}")

        if opt == "LINEMODE":
            supported["linemode"] = True
        elif opt == "TTYPE":
            supported["ttype"] = True
        elif opt == "NEW_ENVIRON":
            supported["new_environ"] = True
        elif opt == "STATUS":
            supported["status"] = True
        elif opt == "NAWS":
            supported["naws"] = True
        elif opt == "BINARY":
            supported["binary"] = True
        elif opt == "ECHO":
            supported["echo"] = True
        elif opt == "SUPPRESS_GO_AHEAD":
            supported["sga"] = True

    return {
        **supported,
        "iac_event_count": len(events),
        "iac_order": order,
    }

from protocol.telnet_client import TelnetClient
from features.extractor import extract_features

def scan_host(host):
    client = TelnetClient(host)
    raw = client.handshake()
    return {"ip": host, "features": extract_features(raw), "banner": raw["banner"]}

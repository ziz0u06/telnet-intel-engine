from concurrent.futures import ThreadPoolExecutor
from scanner.worker import scan_host

def run_scan(targets):
    with ThreadPoolExecutor(max_workers=10) as p:
        return list(p.map(scan_host, targets))

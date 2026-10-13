import re 
from system.executor import run 


ARP_PATTERN = re.compile(
    r"\((?P<ip>[\d.]+)\)\s+"
    r"at\s+(?P<mac>[0-9a-f:]+)\s+"
    r".*?\s+on\s+(?P<iface>\w+)",
    re.IGNORECASE
)

def parse_arp_line(line):
    match = ARP_PATTERN.search(line)
    if not match:
        return None
    return match.groupdict()

def scan_network():
    result = run(["arp", "-an"])

    if not result.ok:
        return []

    devices = []
    for line in result.out.splitlines():
        parsed = parse_arp_line(line)
        if parsed:
            devices.append(parsed)

    return devices
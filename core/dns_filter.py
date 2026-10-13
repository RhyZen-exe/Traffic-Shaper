import re
from pathlib import Path


LEASES_PATTERN = re.compile(
    r"(?P<timestamp>\d+)\s+"
    r"(?P<mac>[0-9a-f:]+)\s+"
    r"(?P<ip>[\d.]+)\s+"
    r"(?P<hostname>\S+)"
    r".*",
    re.IGNORECASE
)

def parse_leases_line(line):
    match = LEASES_PATTERN.search(line)

    if not match:
        return None

    return match.groupdict()

def parse_leases_file(path):
    leases_path = Path(path)

    if not leases_path.exists():
        return []

    lines = leases_path.read_text().splitlines()

    devices = []

    for line in lines:
        parsed = parse_leases_line(line)
        if parsed:
            devices.append(parsed)

    return devices
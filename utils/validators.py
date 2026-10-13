import ipaddress
import re

def is_valid_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

MAC_PATTERN = re.compile(r"[0-9a-f]{2}([:-][0-9a-f]{2}){5}", re.IGNORECASE)

def is_valid_mac(value):
    return bool(MAC_PATTERN.fullmatch(value))

HOSTNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")

def is_valid_hostname(value):
    return bool(HOSTNAME_PATTERN.fullmatch(value))


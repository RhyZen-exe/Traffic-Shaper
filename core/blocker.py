import ipaddress
import shlex

from system.executor import run
from system.iptables_commands import (
    build_block_args,
    build_unblock_args,
    list_rules,
)


def is_valid_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def classify_ip(s: str) -> dict:
    try:
        ip = ipaddress.ip_address(s)
    except ValueError:
        return {"valid": False}

    return {
        "valid": True,
        "version": ip.version,
        "private": ip.is_private,
        "loopback": ip.is_loopback,
        "multicast": ip.is_multicast,
    }


def is_in_network(ip: str, network: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        network_obj = ipaddress.ip_network(network)
        return ip_obj in network_obj
    except ValueError:
        return False


def normalize_ip(ip: str) -> str:
    try:
        ip_obj = ipaddress.ip_address(ip)
        return str(ip_obj)
    except ValueError as e:
        raise ValueError(f"Невалидный IP: {ip}") from e


def block_ip(ip: str) -> dict:
    if not is_valid_ip(ip):
        return {"success": False, "error": f"Невалидный IP: {ip}"}

    args = build_block_args(ip)
    result = run(args)

    if not result.ok:
        return {"success": False, "error": result.err}

    return {
        "success": True,
        "ip": ip,
        "command": shlex.join(args),
    }


def unblock_ip(ip: str) -> dict:
    if not is_valid_ip(ip):
        return {"success": False, "error": f"Невалидный IP: {ip}"}

    args = build_unblock_args(ip)
    result = run(args)

    if not result.ok:
        return {"success": False, "error": result.err}

    return {
        "success": True,
        "ip": ip,
        "command": shlex.join(args),
    }


def list_blocked() -> dict:
    args = list_rules()
    result = run(args)

    if not result.ok:
        return {"success": False, "error": result.err}

    return {
        "success": True,
        "rules": result.out,
    }
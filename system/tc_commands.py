import sys

from system.executor import ExecResult, run


def show_qdiscs(iface: str) -> ExecResult:
    return run(["tc", "qdisc", "show", "dev", iface])


def add_delay(iface: str, ms: int) -> ExecResult:
    return run(
        ["tc", "qdisc", "add", "dev", iface, "root", "netem", "delay", f"{ms}ms"]
    )


def add_loss(iface: str, percent: int) -> ExecResult:
    return run(
        [
            "tc",
            "qdisc",
            "add",
            "dev",
            iface,
            "root",
            "netem",
            "loss",
            f"{percent}%",
        ]
    )


def remove_root(iface: str) -> ExecResult:
    return run(["tc", "qdisc", "del", "dev", iface, "root"])

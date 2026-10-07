import os

from system.executor import run


def is_root() -> bool:
    return os.geteuid() == 0


def require_root() -> None:
    if not is_root():
        raise PermissionError("нужны права root")


def can_sudo() -> bool:
    result = run(["sudo", "-n", "true"])
    return result.ok

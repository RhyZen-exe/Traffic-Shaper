import os
import subprocess
from dataclasses import dataclass


@dataclass
class ExecResult:
    ok: bool
    code: int
    out: str
    err: str


def run(cmd: list[str], timeout: int = 5, cwd: str | None = None) -> ExecResult:
    my_env = os.environ.copy()
    my_env["LC_ALL"] = "C"
    my_env["PATH"] = "/usr/sbin:/sbin:" + my_env.get("PATH", "")

    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=my_env, cwd=cwd
        )
    except FileNotFoundError:
        return ExecResult(False, -1, "", f"Программа не найдена: {cmd[0]}")
    except subprocess.TimeoutExpired:
        return ExecResult(False, -1, "", "Таймаут")
    return ExecResult(r.returncode == 0, r.returncode, r.stdout, r.stderr)

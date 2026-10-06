import os
import subprocess


def run(cmd: list[str], timeout: int = 5, cwd: str | None = None) -> str:
    my_env = os.environ.copy()
    my_env["LC_ALL"] = "C"
    my_env["PATH"] = "/usr/sbin:/sbin:" + my_env.get("PATH", "")

    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=my_env, cwd=cwd
        )
    except FileNotFoundError:
        return "Программа не найдена: " + cmd[0]
    except subprocess.TimeoutExpired:
        return "Таймаут"

    if r.returncode == 0:
        return r.stdout
    else:
        return r.stderr

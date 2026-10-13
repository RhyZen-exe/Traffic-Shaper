import psutil
import platform
from system.executor import run

def process_info(pid: int) -> dict:
    try:
        proc = psutil.Process(pid)
        return {
            "success": True,
            "process": {
            "pid": pid,
            "name": proc.name(),
            "cmdline": proc.cmdline(),
            "status": proc.status(),
            "parent_pid": proc.ppid(),
            "children": [child.pid for child in proc.children()],
            },
        }
    except psutil.NoSuchProcess:
        return {"success": False, "error": f"процесс {pid} не найден"}
    except psutil.AccessDenied:
        return {"success": False, "error": f"доступ к процессу {pid} запрещён"}

def list_processes() -> dict:
    processes = []
    for proc in psutil.process_iter(["pid", "name", "status"]):
        processes.append(proc.info)
    return {"success": True, "count": len(processes), "processes": processes}

def find_processes(name: str) -> dict:
    found = []
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] == name:
            found.append(proc.info)
        return {"success": True, "count": len(found), "processes": found}

def trace_process(cmd: list[str], timeout: int = 5) -> dict:
    if platform.system() == "Linux":
        args = ["strace", "-f", "-e", "trace=open,read,write,connect"] + cmd
    else:
        args = cmd

    result = run(args, timeout=timeout)

    if not result.ok:
        return {"success": False, "error": result.err}

    return {
        "success": True,
        "command": " ".join(args),
        "returncode": result.code,
        "stdout": result.out,
        "stderr": result.err,
    }
    
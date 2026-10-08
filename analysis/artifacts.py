import psutil

def collect_files(pid: int) -> dict:
    try:
        proc = psutil.Process(pid)
        files = [f.path for f in proc.open_files()]
        return {"success": True, "count": len(files), "files": files}
    except psutil.NoSuchProcess:
        return {"success": False, "error": f"процусс {pid} не найден"}
    except psutil.AccessDenied:
        return {"success": False, "error": f"доступ к процессу {pid} запрещен"}

def collect_connections(pid: int) -> dict:
    try:
        proc = psutil.Process(pid)
        conns = []
        for c in proc.connections():
            conns.append({
                "local": f"{c.laddr.ip}:{c.laddr.port}",
                "remote": f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else None,
                "status": c.status,
            })
        return {"success": True, "count": len(conns), "connections": conns}
    except psutil.NoSuchProcess:
        return {"success": False, "error": f"процесс {pid} не найден"}
    except psutil.AccessDenied:
        return {"success": False, "error": f"доступ к процессу {pid} запрещён"}

def collect_artifacts(pid: int) -> dict:
    files_result = collect_files(pid)
    conns_result = collect_connections(pid)

    if not files_result["success"] and not conns_result["success"]:
        return {
            "success": False,
            "error": "не удалось собрать артефакты",
            "details": {
                "files": files_result.get("error"),
                "connections": conns_result.get("error"),
            },
        }

    return {
        "success": True,
        "pid": pid,
        "files": files_result.get("files", []),
        "connections": conns_result.get("connections", []),
    }
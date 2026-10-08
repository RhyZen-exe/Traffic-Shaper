import json
from datetime import datetime
from analysis.behavior import process_info
from analysis.artifacts import collect_files, collect_connections

def build_report(pid: int) -> dict:
    return {
        "timestamp": datetime.now().isoformat(),
        "pid": pid,
        "process":  process_info(pid),
        "files": collect_files(pid),
        "connections": collect_connections(pid),
    }

def save_report(report: dict, path: str = "report.json") -> dict:
    try: 
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return {"success": True, "path": path}
    except OSError as e:
        return {"success": False, "error": str(e)}

def load_report(path: str = "report.json") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {"success": True, "report": json.load(f)}
    except FileNotFoundError:
        return {"success": False, "error": f"файл {path} не найден"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"невалидный JSON: {e}"}
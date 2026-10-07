import yaml
from pathlib import Path

REQUIRED_KEYS= ["interface", "database", "leases_file"]

def load_config(path="config.yaml"):
    config_path = Path(path)

    if not config_path.exists:
        raise FileNotFoundError(f"Конфиг не найден: {path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    missing = [key for key in REQUIRED_KEYS if key not in config]
    if missing:
        raise ValueError(f"В конфиге не хватает ключей: {missing}")

    return config
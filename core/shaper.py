import logging

from system.tc_commands import add_delay, add_limit, add_loss, remove_root
from utils.privileges import require_root

logger = logging.getLogger(__name__)


def apply_delay(iface: str, ms: int) -> None:
    if ms <= 0:
        raise ValueError("мс должен быть >0")
    require_root()
    remove_root(iface)
    r = add_delay(iface, ms)
    if not r.ok:
        raise RuntimeError(f"tc не смог: {r.err}")
    logger.info("delay %dms на %s", ms, iface)


def apply_loss(iface: str, percent: int) -> None:
    if percent <= 0 or percent > 100:
        raise ValueError(f"percent должен быть 1-100, получил {percent}")
    require_root()
    remove_root(iface)
    r = add_loss(iface, percent)
    if not r.ok:
        raise RuntimeError(f"tc не смог: {r.err}")
    logger.info("loss %d%% на %s", percent, iface)


def apply_limit(iface: str, kbps: int) -> None:
    if kbps <= 0:
        raise ValueError(f"kbps: {kbps} должен быть больше 0")
    require_root()
    remove_root(iface)
    r = add_limit(iface, kbps)
    if not r.ok:
        raise RuntimeError(f"tc не смог: {r.err}")
    logger.info("limit %dkbps на %s", kbps, iface)


def reset(iface: str) -> None:
    require_root()
    r = remove_root(iface)
    if not r.ok:
        raise RuntimeError(f"tc не смог: {r.err}")
    logger.info("Сброшены правила на %s", iface)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    iface = "wlp4s0"
    apply_limit(iface, 1000)

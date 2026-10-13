import atexit
import logging
import signal
import sys

from system.tc_commands import remove_root

logger = logging.getLogger(__name__)

_iface: str | None = None


def _do_cleanup() -> None:
    if _iface is None:
        return
    logger.info("Убираю правила tc на %s", _iface)
    r = remove_root(_iface)
    if not r.ok:
        logger.warning("Не удалось убрать: %s", r.err)


def _on_signal(signum, frame) -> None:
    logger.warning("Получен сигнал %s, выходим", signum)
    sys.exit(0)


def install_handlers(iface: str) -> None:
    global _iface
    _iface = iface
    signal.signal(signal.SIGINT, _on_signal)
    signal.signal(signal.SIGTERM, _on_signal)
    atexit.register(_do_cleanup)
    logger.info("Обработчики установлены для %s", iface)

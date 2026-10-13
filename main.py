import argparse
import logging

from core.cleanup import install_handlers
from core.shaper import apply_delay, apply_limit, apply_loss, reset

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Traffic-Shaper: управление трафиком")
    parser.add_argument("--iface", default="wlp4s0", help="Сетевой интерфейс")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show", help="Показать правила")

    p_delay = subparsers.add_parser("delay", help="добавить задержку")
    p_delay.add_argument("--ms", type=int, required=True, help="...")

    p_loss = subparsers.add_parser("loss", help="добавить потерю пакетов")
    p_loss.add_argument("--percent", type=int, required=True, help="...")

    p_limit = subparsers.add_parser("limit", help="добавить лимит kbps")
    p_limit.add_argument("--kbps", type=int, required=True, help="...")

    subparsers.add_parser("reset", help="Сбросить правила")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.command != "show":
        install_handlers(args.iface)

    if args.command == "show":
        from system.tc_commands import show_qdiscs

        r = show_qdiscs(args.iface)
        print(r.out)
    elif args.command == "delay":
        apply_delay(args.iface, args.ms)
    elif args.command == "loss":
        apply_loss(args.iface, args.percent)
    elif args.command == "limit":
        apply_limit(args.iface, args.kbps)
    elif args.command == "reset":
        reset(args.iface)


if __name__ == "__main__":
    main()

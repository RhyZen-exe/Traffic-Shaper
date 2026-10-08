def build_block_args(ip: str ) -> list[str]:
    return ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP" ]


def build_unblock_args(ip: str ) -> list[str]:
    return ["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP" ]


def list_rules() -> list[str]:
    return ["iptables", "-L", "INPUT", "-n", "--line-numbers"]

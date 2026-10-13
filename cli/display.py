def show_devices(devices):
    if not devices:
        print("Нет устройств для отображения")
        return 

    print(f"{'IP':<18}{'MAC':<20}{'HOSTNAME':<20}{'STATUS':<10}")
    print("-" * 68)

    for d in devices:
        ip = d.get("ip", "-")
        mac = d.get("mac", "-")
        hostname = d.get("hostname", "-")
        status = d.get("status", "-")
        print(f"{ip:<18}{mac:<20}{hostname:<20}{status:<10}")
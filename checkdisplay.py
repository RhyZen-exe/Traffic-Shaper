from core.devices import parse_arp_line

# обычная строка
line = "? (192.168.12.5) at aa:bb:cc:dd:ee:ff [ether] on wlan0"
print(parse_arp_line(line))

# мусор → None
print(parse_arp_line("мусор без данных"))

# <incomplete> → тоже None
line3 = "? (192.168.12.10) at <incomplete> on wlan0"
print(parse_arp_line(line3))

# Traffic-Shaper

Linux CLI-утилита для управления сетевым трафиком через `tc`. Имитирует задержки, потери пакетов и ограничивает скорость на сетевом интерфейсе.

## Что умеет

- **Задержка (`delay`)** — добавляет задержку к пакетам на интерфейсе.
- **Потери (`loss`)** — имитирует потерю пакетов.
- **Ограничение скорости (`limit`)** — ограничивает скорость интерфейса через `tbf`.
- **Просмотр (`show`)** — показывает текущие правила `tc`.
- **Сброс (`reset`)** — удаляет все правила с интерфейса.
- **Уборка по сигналу** — при `Ctrl+C` или `SIGTERM` правила `tc` удаляются автоматически.

## Требования

- **ОС:** Linux (на Windows — через WSL2)
- **Права:** root (sudo) — для `tc`
- **Утилиты:** `tc` (из пакета `iproute2`)
- **Python:** 3.10+

## Установка

```bash
git clone https://github.com/RhyZen-exe/Traffic-Shaper.git
cd Traffic-Shaper
pip install -r requirements.txt
```

## Использование

Все команды требуют `sudo`. По умолчанию используется интерфейс `wlp4s0`.

### Показать текущие правила

```bash
sudo python main.py show
```

### Добавить задержку 100 мс

```bash
sudo python main.py delay --ms 100
```

### Имитировать 10% потерь

```bash
sudo python main.py loss --percent 10
```

### Ограничить скорость до 1000 кбит/с

```bash
sudo python main.py limit --kbps 1000
```

### Сбросить все правила

```bash
sudo python main.py reset
```

### Указать другой интерфейс

Общий аргумент `--iface` указывается **до** имени команды:

```bash
sudo python main.py --iface eno1 delay --ms 100
```

## Проверка эффекта

```bash
# Применить задержку 300 мс
sudo python main.py delay --ms 300

# Пинг покажет задержку ~415 мс вместо ~115 мс
ping -c 3 8.8.8.8

# Убрать задержку
sudo python main.py reset
```

## Структура проекта

```
Traffic-Shaper/
├── main.py                  # CLI: точка входа (argparse)
├── config.yaml              # настройки
├── requirements.txt         # зависимости
├── LICENSE                  # лицензия
│
├── system/                  # низкоуровневая работа с Linux
│   ├── executor.py          # обёртка над subprocess
│   ├── tc_commands.py       # команды tc
│   └── iptables_commands.py # команды iptables
│
├── core/                    # логика проекта
│   ├── shaper.py            # управление tc
│   ├── blocker.py           # блокировка IP через iptables
│   ├── devices.py           # обнаружение устройств (arp)
│   ├── dns_filter.py        # парсинг dnsmasq.leases
│   ├── storage.py           # SQLite (devices, rules)
│   └── cleanup.py           # уборка по сигналу
│
├── analysis/                # анализ поведения процессов
│   ├── behavior.py          # psutil: процессы
│   ├── artifacts.py         # psutil: файлы и соединения
│   └── report.py            # JSON-отчёт
│
├── cli/                     # интерфейс командной строки
│   └── display.py           # вывод таблиц
│
├── utils/                   # вспомогательное
│   ├── privileges.py        # проверка root
│   └── validators.py        # проверки IP/MAC/hostname
│
└── tests/                   # тесты
    ├── test_config.py
    └── test_storage.py
```

## Авторы

- **RhyZen.exe**
- **Zerka**
- **afkcenter**

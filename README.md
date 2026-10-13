# Traffic-Shaper

Linux CLI-утилита для управления сетевым трафиком через `tc`. Имитирует задержки, потери пакетов и ограничивает скорость на сетевом интерфейсе.

## Что умеет

- **Задержка (`delay`)** — добавляет задержку к пакетам на интерфейсе.
- **Потери (`loss`)** — имитирует потерю пакетов.
- **Ограничение скорости (`limit`)** — ограничивает скорость интерфейса через `tbf`.
- **Просмотр (`show`)** — показывает текущие правила `tc`.
- **Сброс (`reset`)** — удаляет все правила с интерфейса.
- **Автоуборка** — правила удаляются автоматически при выходе (Ctrl+C или `SIGTERM`).

## Требования

- **ОС:** Linux
- **Права:** root (sudo) — для `tc`.
- **Утилиты:** `tc` (из пакета `iproute2`).
- **Python:** 3.10+.

## Установка

```bash
git clone https://github.com/RhyZen-exe/Traffic-Shaper.git
cd Traffic-Shaper
pip install -r requirements.txt
```

## Использование

Все команды требуют `sudo`.

### Показать текущие правила

```bash
sudo python main.py show --iface wlp4s0
```

### Добавить задержку 100 мс

```bash
sudo python main.py delay --iface wlp4s0 --ms 100
```

### Имитировать 10% потерь

```bash
sudo python main.py loss --iface wlp4s0 --percent 10
```

### Ограничить скорость до 1000 кбит/с

```bash
sudo python main.py limit --iface wlp4s0 --kbps 1000
```

### Сбросить все правила

```bash
sudo python main.py reset --iface wlp4s0
```

## Проверка эффекта

```bash
# Применить задержку 300 мс
sudo python main.py delay --iface wlp4s0 --ms 300

# Пинг покажет задержку ~415 мс вместо ~115 мс
ping -c 3 8.8.8.8

# Убрать задержку
sudo python main.py reset --iface wlp4s0
```

## Структур# README — пишем вместе. Но сначала — проверка

Ты сказал "всё сделал". **Проверим:**

**1.** Запусти 6 команд:

```bash
sudo PYTHONPATH=. python main.py --help
sudo PYTHONPATH=. python main.py show
sudo PYTHONPATH=. python main.py delay --iface wlp4s0 --ms 100
sudo PYTHONPATH=. python main.py loss --iface wlp4s0 --percent 10
sudo PYTHONPATH=. python main.py limit --iface wlp4s0 --kbps 1000
sudo PYTHONPATH=. python main.py reset --iface wlp4s0
```

**2.** Пришли **вывод `--help`** — там должно быть **5 команд** (`show`, `delay`, `loss`, `limit`, `reset`), **без дубликата**.

Если всё работает — **идём к README**. Если нет — **разберём сначала**.

---

## README — что мне нужно от тебя

**Я уже писал черновик** (в сообщении ~15 назад). Ты **не подтвердил** 2 вещи:

### 1. Команды в README

**5 команд.** Пример:

```bash
sudo python main.py show --iface wlp4s0
sudo python main.py delay --iface wlp4s0 --ms 100
sudo python main.py loss --iface wlp4s0 --percent 10
sudo python main.py limit --iface wlp4s0 --kbps 1000
sudo python main.py reset --iface wlp4s0
```

**Согласен** с этим? Или **что-то поменять**?

### 2. Структура проекта

**У вас сейчас:**

```
Traffic-Shaper/
├── main.py
├── config.yaml
├── requirements.txt
├── LICENSE
├── README.md
│
├── system/
│   ├── executor.py
│   ├── tc_commands.py
│   └── iptables_commands.py
│
├── core/
│   ├── shaper.py
│   ├── blocker.py
│   ├── devices.py
│   ├── storage.py
│   ├── dns_filter.py
│   └── cleanup.py
│
├── cli/
│   └── display.py
│
├── analysis/
│   ├── behavior.py
│   ├── artifacts.py
│   └── report.py
│
├── utils/
│   ├── privileges.py
│   ├── validators.py
│   └── logger.py   ← есть?
│
└── tests/
    ├── test_config.py
    └── test_storage.py
```

**Проверь:** всё ли **правильно**? Что **есть** `logger.py`? Что **есть** `tests/test_config.py` и `test_storage.py` — **реально работают** или **пустые**?

---

## Готовый README — вот он

**Вот финальная версия.** **Проверь**, что **всё соответствует** вашему проекту. Если **что-то не так** — **скажи**, я поправлю.

---

```markdownа проекта

```

Traffic-Shaper/
├── main.py # CLI: точка входа (argparse)
├── config.yaml # настройки проекта
├── requirements.txt # зависимости
├── LICENSE # лицензия
│
├── system/ # низкоуровневая работа с Linux
│ ├── executor.py # обёртка над subprocess
│ ├── tc_commands.py # команды tc
│ └── iptables_commands.py # команды iptables
│
├── core/ # логика проекта
│ ├── shaper.py # управление tc
│ ├── blocker.py # блокировка IP через iptables
│ ├── devices.py # обнаружение устройств (arp)
│ ├── dns_filter.py # парсинг dnsmasq.leases
│ ├── storage.py # SQLite (devices, rules)
│ └── cleanup.py # уборка при выходе
│
├── analysis/ # анализ поведения процессов
│ ├── behavior.py # psutil: процессы
│ ├── artifacts.py # psutil: файлы и соединения
│ └── report.py # JSON-отчёт
│
├── cli/ # интерфейс командной строки
│ └── display.py # вывод таблиц
│
├── utils/ # вспомогательное
│ ├── privileges.py # проверка root
│ └── validators.py # проверки IP/MAC/hostname
│
└── tests/ # тесты
├── test_config.py
└── test_storage.py

```

## Авторы

- **RhyZen.exe**
- **Zerka**
- **afkcenter**
```

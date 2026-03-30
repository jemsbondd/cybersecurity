#!/usr/bin/env python3
"""
=============================================================
  CTF Wordlist Generator — Universal Script v2
=============================================================
Шаги:
  1. Введи префикс (известное ДО неизвестного)
  2. Введи суффикс (известное ПОСЛЕ, если есть)
  3. Введи количество неизвестных символов
  4. Выбери тип символов: цифры / буквы / оба / произвольный
  5. Генерация → wordlist.txt
=============================================================
"""

import itertools
import string
import os
import sys


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 54)
    print("   🔑  CTF Universal Wordlist Generator v2")
    print("=" * 54)
    print()


def ask(prompt, validator=None, error_msg="Некорректный ввод."):
    while True:
        val = input(prompt).strip()
        if validator is None or validator(val):
            return val
        print(f"  ❌  {error_msg}")


def choose_charset() -> tuple:
    DIGITS  = string.digits                              # 0-9
    LOWER   = string.ascii_lowercase                    # a-z
    UPPER   = string.ascii_uppercase                    # A-Z
    RU_LOW  = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    RU_UP   = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    SPECIAL = string.punctuation                        # !@#$%...

    OPTIONS = {
        "1":  ("Цифры (0-9)",                          DIGITS),
        "2":  ("Строчные латинские (a-z)",             LOWER),
        "3":  ("Заглавные латинские (A-Z)",            UPPER),
        "4":  ("Все латинские (a-z + A-Z)",            LOWER + UPPER),
        "5":  ("Строчные русские (а-я)",               RU_LOW),
        "6":  ("Заглавные русские (А-Я)",              RU_UP),
        "7":  ("Все русские (а-я + А-Я)",              RU_LOW + RU_UP),
        "8":  ("Цифры + строчные латинские",           DIGITS + LOWER),
        "9":  ("Цифры + все латинские",                DIGITS + LOWER + UPPER),
        "10": ("Цифры + строчные русские",             DIGITS + RU_LOW),
        "11": ("Цифры + буквы лат. + спецсимволы",    DIGITS + LOWER + UPPER + SPECIAL),
        "12": ("Произвольный набор (введи сам)",       None),
    }

    print("─" * 54)
    print("  Шаг 3. Символы для НЕИЗВЕСТНОЙ части")
    print("─" * 54)
    print()
    print("  Только один тип:")
    print("  [1]  Цифры              (0-9)")
    print("  [2]  Строчные латинские (a-z)")
    print("  [3]  Заглавные латинские(A-Z)")
    print("  [4]  Все латинские      (a-z + A-Z)")
    print("  [5]  Строчные русские   (а-я)")
    print("  [6]  Заглавные русские  (А-Я)")
    print("  [7]  Все русские        (а-я + А-Я)")
    print()
    print("  Комбинации:")
    print("  [8]  Цифры + строчные латинские")
    print("  [9]  Цифры + все латинские")
    print("  [10] Цифры + строчные русские")
    print("  [11] Цифры + латинские + спецсимволы")
    print()
    print("  [12] Произвольный — введи символы сам")
    print("       (например: 12bw$  — порядок не важен)")
    print()

    choice = ask(
        "  Ваш выбор (1-12): ",
        lambda v: v in OPTIONS,
        "Введи число от 1 до 12."
    )

    name, charset = OPTIONS[choice]

    if charset is None:
        raw = ask(
            "  Введи символы (дубли уберутся автоматически): ",
            lambda v: len(v.strip()) > 0,
            "Нельзя оставить пустым."
        )
        charset = "".join(dict.fromkeys(raw.strip()))
        name = f"Произвольный: '{charset}'"

    print(f"\n  ✅  Выбрано: {name}")
    print(f"      Символов в наборе: {len(charset)}")
    return name, charset


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def generate(prefix: str, suffix: str, length: int, charset: str, filepath: str) -> int:
    total = len(charset) ** length
    print(f"\n  📊  Всего комбинаций: {fmt(total)}")

    if total > 50_000_000:
        entry_len = len(prefix) + length + len(suffix) + 1
        mb = total * entry_len / 1_048_576
        print(f"  ⚠️   Файл займёт ~{mb:.0f} МБ. Продолжить? (y/n): ", end="")
        if input().strip().lower() != "y":
            print("  Отменено.")
            sys.exit(0)

    print(f"  ⚙️   Генерация...", end=" ", flush=True)

    with open(filepath, "w", encoding="utf-8") as f:
        for i, combo in enumerate(itertools.product(charset, repeat=length), 1):
            f.write(prefix + "".join(combo) + suffix + "\n")
            if i % 1_000_000 == 0:
                print(f"{fmt(i)}...", end=" ", flush=True)

    print("✅  Готово!")
    return total


def main():
    clear()
    banner()

    # ── Шаг 1 & 2: фикса ──────────────────────────────────────
    print("─" * 54)
    print("  Шаг 1. Известная (фиксированная) часть")
    print("─" * 54)
    print("  Если неизвестное — в конце:     prefix = 'FLAG_' , suffix = ''")
    print("  Если неизвестное — в середине:  prefix = 'FLAG{' , suffix = '}'")
    print("  Если неизвестное — в начале:    prefix = ''      , suffix = '_2024'")
    print()

    prefix = input("  Префикс (известное ДО, или Enter если нет): ")
    suffix = input("  Суффикс (известное ПОСЛЕ, или Enter если нет): ")
    mask   = prefix + "?" * 3 + suffix
    print(f"\n  Маска выглядит так: '{mask}'  (??? = неизвестное)")
    print()

    # ── Шаг 2: длина ──────────────────────────────────────────
    print("─" * 54)
    print("  Шаг 2. Длина неизвестной части")
    print("─" * 54)
    length_str = ask(
        "  Сколько неизвестных символов? (1-10): ",
        lambda v: v.isdigit() and 1 <= int(v) <= 10,
        "Введи число от 1 до 10."
    )
    length = int(length_str)
    print(f"  ✅  {length} символ(ов). Маска: '{prefix + '?' * length + suffix}'")
    print()

    # ── Шаг 3: набор символов ─────────────────────────────────
    _, charset = choose_charset()
    print()

    # ── Шаг 4: файл ───────────────────────────────────────────
    print("─" * 54)
    print("  Шаг 4. Сохранение")
    print("─" * 54)
    default_name = "wordlist.txt"
    out_name = input(f"  Имя файла [{default_name}]: ").strip() or default_name
    if not out_name.endswith(".txt"):
        out_name += ".txt"

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_name)

    # ── Генерация ──────────────────────────────────────────────
    print()
    total = generate(prefix, suffix, length, charset, out_path)

    # ── Итог ──────────────────────────────────────────────────
    size = os.path.getsize(out_path)
    size_str = f"{size/1024:.1f} КБ" if size < 1_048_576 else f"{size/1_048_576:.1f} МБ"

    print()
    print("─" * 54)
    print(f"  📁  Файл:   {out_path}")
    print(f"  📝  Строк:  {fmt(total)}")
    print(f"  💾  Размер: {size_str}")
    print("─" * 54)

    print("\n  👀  Первые 10 строк:")
    with open(out_path, encoding="utf-8") as f:
        for j, line in enumerate(f):
            if j >= 10: break
            print(f"      {line}", end="")
    print("\n      ...")
    print()

    wl = out_name
    print("═" * 54)
    print("  📌  ИНСТРУМЕНТЫ ДЛЯ ИСПОЛЬЗОВАНИЯ WORDLIST'А")
    print("═" * 54)

    print("""
  ┌─────────────────────────────────────────────┐
  │  1. HASHCAT — взлом хешей (MD5, SHA, bcrypt)│
  └─────────────────────────────────────────────┘
  Установка:
    Linux:   sudo apt install hashcat
    Windows: скачать hashcat.net/hashcat → распаковать
    Kali:    уже установлен

  Использование:""")
    print(f"    hashcat -a 0 -m 0    hash.txt {wl}   # MD5")
    print(f"    hashcat -a 0 -m 100  hash.txt {wl}   # SHA1")
    print(f"    hashcat -a 0 -m 1800 hash.txt {wl}   # SHA512")
    print(f"    hashcat -a 0 -m 3200 hash.txt {wl}   # bcrypt")
    print("""
  Ключи:
    -a 0     = атака по словарю (наш случай)
    -m XXXX  = тип хеша (hashcat --help | grep SHA)
    --show   = показать уже взломанные
    --force  = игнорировать предупреждения (на ВМ)
""")

    print("""  ┌─────────────────────────────────────────────┐
  │  2. JOHN THE RIPPER — хеши + архивы/файлы  │
  └─────────────────────────────────────────────┘
  Установка:
    Linux:   sudo apt install john
    Windows: github.com/openwall/john → Releases
    Kali:    уже установлен

  Использование:""")
    print(f"    john --wordlist={wl} hash.txt")
    print(f"    john --wordlist={wl} --format=raw-md5 hash.txt")
    print(f"    john --wordlist={wl} --format=raw-sha1 hash.txt")
    print("""
  Дополнительно (извлечь хеш из файла):
    zip2john  archive.zip  > hash.txt  → потом john
    pdf2john  file.pdf     > hash.txt
    ssh2john  id_rsa       > hash.txt
    john --show hash.txt               → показать результат
""")

    print("""  ┌─────────────────────────────────────────────┐
  │  3. HYDRA — брутфорс сетевых сервисов      │
  └─────────────────────────────────────────────┘
  Установка:
    Linux:   sudo apt install hydra
    Windows: github.com/maaaaz/thc-hydra-windows
    Kali:    уже установлен

  Использование:""")
    print(f"    hydra -l admin -P {wl} 192.168.1.1 ssh")
    print(f"    hydra -l admin -P {wl} 192.168.1.1 ftp")
    print(f"    hydra -l admin -P {wl} 192.168.1.1 rdp")
    print(f"    hydra -l admin -P {wl} http-post-form '/login:user=^USER^&pass=^PASS^:F=incorrect'")
    print("""
  Ключи:
    -l admin   = один логин
    -L list.txt= список логинов
    -P         = наш wordlist с паролями
    -t 4       = потоков (не перегружать!)
    -V         = verbose (видеть каждую попытку)
""")

    print("""  ┌─────────────────────────────────────────────┐
  │  4. FFUF — брутфорс веб (директории, CTF)  │
  └─────────────────────────────────────────────┘
  Установка:
    Linux:   sudo apt install ffuf
             или: go install github.com/ffuf/ffuf/v2@latest
    Windows: github.com/ffuf/ffuf → Releases → .exe
    Kali:    уже установлен

  Использование:""")
    print(f"    ffuf -w {wl} -u http://target/FUZZ")
    print(f"    ffuf -w {wl} -u http://target/FUZZ.php")
    print(f"    ffuf -w {wl} -u http://target/?id=FUZZ")
    print(f"    ffuf -w {wl} -u http://target/ -H 'X-Token: FUZZ'")
    print("""
  Ключи:
    FUZZ       = место подстановки слова из списка
    -fc 404    = фильтр: скрыть 404 ответы
    -mc 200    = показывать только 200 OK
    -t 50      = потоков
    -o out.json= сохранить результат
""")

    print("""  ┌─────────────────────────────────────────────┐
  │  5. GOBUSTER — альтернатива ffuf для веба  │
  └─────────────────────────────────────────────┘
  Установка:
    Linux:   sudo apt install gobuster
             или: go install github.com/OJ/gobuster/v3@latest
    Kali:    уже установлен

  Использование:""")
    print(f"    gobuster dir -u http://target -w {wl}")
    print(f"    gobuster dir -u http://target -w {wl} -x php,html,txt")
    print(f"    gobuster dns -d target.com    -w {wl}   # субдомены")
    print("""
  Ключи:
    dir        = режим директорий
    dns        = режим субдоменов
    -x         = расширения файлов для проверки
    -t 30      = потоков
    -o out.txt = сохранить результат
""")
    print("═" * 54)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  ⛔  Прервано.")
        sys.exit(0)

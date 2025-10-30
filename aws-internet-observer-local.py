# home_update.py
import requests
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the same directory as the script
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(env_path)

API_URL = os.getenv("API_URL", "https://localhost/api/update-ip")
TOKEN = os.getenv("API_TOKEN", "change_this_to_a_random_token")
INTERVAL = int(os.getenv("UPDATE_INTERVAL", "300"))  # seconds

def get_public_ip():
    try:
        return requests.get("https://ifconfig.co/ip", timeout=5).text.strip()
    except:
        try:
            return requests.get("https://api.ipify.org", timeout=5).text.strip()
        except:
            return None

def push_ip(ip):
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type":"application/json"}
    try:
        r = requests.post(API_URL, json={"ip": ip}, headers=headers, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    while True:
        ip = get_public_ip()
        if ip:
            sc, txt = push_ip(ip)
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "ip:", ip, "resp:", sc)
        else:
            print("could not determine public ip")
        time.sleep(INTERVAL)

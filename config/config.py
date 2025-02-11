import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNT_FILE = os.path.join(BASE_DIR, "../data/accounts.txt")
PROXY_FILE = os.path.join(BASE_DIR, "../data/proxy.txt")
REGIST_FILE = os.path.join(BASE_DIR, "../data/register.txt")
CONFIG_FILE = os.path.join(BASE_DIR, "../config/config.json")
NET_FILE = os.path.join(BASE_DIR, "../config/networks.json")
API_URL = "https://referralapi.layeredge.io/api"

def get_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)
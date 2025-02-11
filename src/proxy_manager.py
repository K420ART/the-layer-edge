from config.config import PROXY_FILE
from utils.logger import logging
import os

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    async def load_proxies(self):
        try:
            if not os.path.exists(PROXY_FILE):
                logging(f"File {PROXY_FILE} Not Found.")
                return
            
            with open(PROXY_FILE, 'r') as f:
                self.proxies = f.read().splitlines()
            
            if not self.proxies:
                return
        
        except Exception as e:
            logging(f"Failed To Load Proxies: {e}")
            self.proxies = []

    def check_proxy_schemes(self, proxy):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxy.startswith(scheme) for scheme in schemes):
            return proxy
        return f"http://{proxy}"

    def get_next_proxy_for_account(self, address):
        if address not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[address] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[address]

    def rotate_proxy_for_account(self, address):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[address] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
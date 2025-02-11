import json, time, asyncio
from eth_account.messages import encode_defunct
from eth_account import Account
from config.config import get_config
from utils.utils import masked
from utils.colors import *
from utils.logger import logging, e_logs
from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession, ClientTimeout, ClientResponseError
from src.headers import headers
from image.gen_ua import UserAgentGenerator

class APIClient:
    def __init__(self):
        self.base_headers = headers()
        self.config = get_config()
        self.generator = UserAgentGenerator(device_type='android', browser_type='chrome')
        self.referral = self.config["referral_code"]

    async def daily_checkin(self, index: int, account: str, address: str, proxy=None, retries=5):
        url = "https://referralapi.layeredge.io/api/light-node/claim-node-points"
        data = json.dumps(self.generate_checkin_payload(account, address))
        headers = {
            **self.base_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "User-Agent": self.generator.generate()
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 405:
                            logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Already Checked-In Today")
                            return 
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Check-In Failed", log_type="error")
                e_logs(f"{e}")
                return 
            

    async def node_status(self, index: int, address: str, proxy=None, retries=5):
        url = f"https://referralapi.layeredge.io/api/light-node/node-status/{address}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.get(url=url, headers=self.base_headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Failed to get node status", log_type="error")
                e_logs(f"{e}")
                return 

    async def start_node(self, index: int, account: str, address: str, proxy=None, retries=5):
        url = f"https://referralapi.layeredge.io/api/light-node/node-action/{address}/start"
        data = json.dumps(self.generate_node_payload(account, address, "activation"))
        headers = {
            **self.base_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "User-Agent": self.generator.generate()
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Failed to start node", log_type="error")
                e_logs(f"{e}")
                return 

    async def stop_node(self, index: int, account: str, address: str, proxy=None, retries=5):
        url = f"https://referralapi.layeredge.io/api/light-node/node-action/{address}/stop"
        data = json.dumps(self.generate_node_payload(account, address, "deactivation"))
        headers = {
            **self.base_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "User-Agent": self.generator.generate()
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Stopping node successfully", log_type="success")
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Failed to stop node", log_type="error")
                e_logs(f"{e}")
                return 

    async def user_confirm(self, index: int, address: str, proxy=None):
        url = f"https://referralapi.layeredge.io/api/referral/register-wallet/{self.referral}"
        data = json.dumps({"walletAddress": address})
        headers = {
            **self.base_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "User-Agent": self.generator.generate()
        }

        await asyncio.sleep(5)

        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Error during confirmation", log_type="error")
            e_logs(f"{e}")
            return None

    async def user_data(self, index: int, address: str, proxy=None):
        url = f"https://referralapi.layeredge.io/api/referral/wallet-details/{address}"

        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                async with session.get(url=url, headers=self.base_headers) as response:
                    if response.status == 404:
                        logging(f" {YELLOW}{index:<4}{RESET} | {masked(address)} not found, try to register...")

                        result = await self.user_confirm(index, address, proxy)
                        if not result:
                            return None

                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Successfully registered address", log_type="success")
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Waiting for confirmation...")
                        await asyncio.sleep(10)
                        return await self.user_data(index, address, proxy)

                    response.raise_for_status()
                    result = await response.json()
                    return result.get('data', None)

        except ClientResponseError as e:
            if e.status == 409:
                logging(f" {YELLOW}{index:<4}{RESET} | Address {masked(address)} already registered, Skipping", log_type="warning")
                e_logs(f"{e}")
                return None
            logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Error fetching user data", log_type="error")
            e_logs(f"{e}")
            return None
        except Exception as e:
            logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Unexpected error", log_type="error")
            e_logs(f"{e}")
            return None

    def generate_checkin_payload(self, account: str, address: str):
        timestamp = int(time.time() * 1000)
        try:
            message = f"I am claiming my daily node point for {address} at {timestamp}"
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = signed_message.signature.hex()
            data = {"sign":f"0x{signature}", "timestamp":timestamp, "walletAddress":address}
            return data
        except Exception as e:
            return None

    def generate_node_payload(self, account: str, address: str, msg_type: str):
        timestamp = int(time.time() * 1000)
        try:
            message = f"Node {msg_type} request for {address} at {timestamp}"
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = signed_message.signature.hex()
            data = {"sign":f"0x{signature}", "timestamp":timestamp}
            return data
        except Exception as e:
            return None
import asyncio, os, readchar
from colorama import init
from config.config import ACCOUNT_FILE, REGIST_FILE, get_config
from utils.utils import clear, ascii, masked, time_remain
from utils.logger import logging, e_logs
from utils.colors import *
from src.proxy_manager import ProxyManager
from image.gen_qnet import X9A2B
from src.wallet_manager import WalletManager
from src.api_client import APIClient
from src.node_manager import NodeManager

init(autoreset=True)

class LayerEdge:
    def __init__(self, ACCOUNT_FILE):
        self.account_file = ACCOUNT_FILE
        self.regist_file = REGIST_FILE
        self.config = get_config()
        self.referral = self.config["referral_code"]
        self.retry = self.config["retry_count"]
        self.MAX_THREADS = self.config["MAX_THREADS"]
        self.proxy_manager = ProxyManager()
        self.wallet_manager = WalletManager(self.account_file)
        self.api_client = APIClient()
        self.node_manager = NodeManager(self.api_client, self.proxy_manager)

    async def d3d_menu(self, accounts):
        selected_option = 0
        
        menu_options = [
            f"1. {GREEN}Run Node            {BLUE}[With Proxy]",
            f"2. {GREEN}Run Node            {BLACK}[Without Proxy]",
            f"3. {GREEN}Register Account    {BLUE}[with Proxy]",
            f"4. {GREEN}Register Account    {BLACK}[without Proxy]",
            f"5. {GREEN}Generate & Register {BLUE}[with Proxy]",
            f"6. {GREEN}Generate & Register {BLACK}[without Proxy]",
        ]

        while True:
            clear()
            ascii()
            await self.proxy_manager.load_proxies()

            accounts_info = f"Accounts.txt : {len(accounts)} private key found"
            proxies_info = f"Proxy.txt    : {len(self.proxy_manager.proxies)} proxies found"
            referral = f"Referral     : {self.referral}"
            max_threads_count = f"Max Threads  : {self.MAX_THREADS}"

            max_length = max(len(accounts_info), len(proxies_info), len(referral))
            
            print(f"\n{BLACK}╔{'═' * (max_length + 2)}╗{RESET}")
            print(f"{BLACK}║ {Fore.WHITE + Style.NORMAL}{accounts_info.ljust(max_length)} {BLACK}║{RESET}")
            print(f"{BLACK}║ {Fore.WHITE + Style.NORMAL}{proxies_info.ljust(max_length)} {BLACK}║{RESET}")
            print(f"{BLACK}║ {Fore.WHITE + Style.NORMAL}{referral.ljust(max_length)} {BLACK}║{RESET}")
            print(f"{BLACK}║ {Fore.WHITE + Style.NORMAL}{max_threads_count.ljust(max_length)} {BLACK}║{RESET}")
            print(f"{BLACK}╚{'═' * (max_length + 2)}╝{RESET}")
            print(GREEN + f"\n [?] {BLACK}choose menu :") 
            print(f"{BLACK}╔{'═' * 48}╗{RESET}")
            for i, option in enumerate(menu_options):
                if i == selected_option:
                    print(f"{GREEN}║ {WHITE}➤ {option.ljust(54)} {GREEN}║{RESET}")
                else:
                    print(f"{BLACK}║ {WHITE}  {option.ljust(54)} {BLACK}║{RESET}")
            print(f"{BLACK}╚{'═' * 48}╝{RESET}\n")

            print(f"{WHITE} ⇅ Use arrow keys to navigate, Enter to select", end="\r" , flush=True)

            key = readchar.readkey()
            if key == readchar.key.UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif key == readchar.key.DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif key == readchar.key.LEFT:
                selected_option = (selected_option - 1) % len(menu_options)
            elif key == readchar.key.RIGHT:
                selected_option = (selected_option + 1) % len(menu_options)
            elif key == readchar.key.ENTER:
                choose = selected_option + 1
                if choose in [1, 2, 3, 4, 5, 6]:
                    menu_type = (
                        "Run node on all accounts with proxy" if choose == 1 else 
                        "Run node on all accounts without proxy" if choose == 2 else
                        "Register from file register.txt with proxy" if choose == 3 else
                        "Register from file register.txt without proxy" if choose == 4 else
                        "Generate wallet & register with with proxy" if choose == 5 else
                        "Generate wallet & register with without proxy"
                    )
                    
                    print(f"  - {menu_type} selected")
                    
                    if choose in [5, 6]:
                        num_wallets = int(input(f"  - How many wallets would you like to generate? {GREEN}").strip())
                        logging(BLACK + f"~" * 38)
                        logging(f"Generating {num_wallets} wallets...")
                        return choose, num_wallets
                    return choose, None
            else:
                print(f"  {RED}Invalid input. Use arrow keys to navigate.")
                await asyncio.sleep(1)

    async def process_registration(self, index: int, account: str, use_proxy: bool):
        address = self.wallet_manager.generate_address(account)
        proxy = self.proxy_manager.get_next_proxy_for_account(address) if use_proxy else None

        user = None
        retry_count = 0
        while user is None and retry_count < self.retry:
            user = await self.api_client.user_data(index, address, proxy)
            if user:
                logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} is already registered, moving to accounts.txt", log_type="success")
                with open(self.account_file, 'a') as account_file:
                    account_file.write(f"{account}\n")
                with open(self.regist_file, 'r') as file:
                    lines = file.readlines()
                with open(self.regist_file, 'w') as file:
                    file.writelines(line for line in lines if line.strip() != account)
                return True
            else:
                logging(f" {YELLOW}{index:<4}{RESET} | Registering Address: {masked(address)}")
                register = await self.api_client.user_confirm(index, address, proxy)
                if register:
                    logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Successfully Registered", log_type="success")
                    await asyncio.sleep(10)
                    
                    check_in = await self.api_client.daily_checkin(index, account, address, proxy)
                    if check_in and check_in.get("message") == "node points claimed successfully":
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Checked-In Successfully", log_type="success")
                        
                        with open(self.account_file, 'a') as account_file:
                            account_file.write(f"{account}\n")
                        
                        with open(self.regist_file, 'r') as file:
                            lines = file.readlines()
                        with open(self.regist_file, 'w') as file:
                            file.writelines(line for line in lines if line.strip() != account)
                        return True
                else:
                    retry_count += 1
                    if retry_count < self.retry:
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address):<1} Attempt {retry_count} failed. Retrying...")
                        await asyncio.sleep(5)
        
        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address):<1} Failed to get data.", log_type="error")
        return False

    async def process_accounts(self, index: int, account: str, use_proxy: bool):
            address = self.wallet_manager.generate_address(account)
            proxy = self.proxy_manager.get_next_proxy_for_account(address) if use_proxy else None

            user = None
            retry_count = 0
            while user is None and retry_count < self.retry:
                user = await self.api_client.user_data(index, address, proxy)
                if user:
                    
                    points = user['nodePoints']
                    logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address):<1} Earned Points: {points:<8}")
                    
                    check_in = await self.api_client.daily_checkin(index, account, address, proxy)
                    if check_in and check_in.get("message") == "node points claimed successfully":
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address):<1} Checked-In Successfully", log_type="success")

                    reconnect_time = await self.node_manager.handle_node_reconnection(index, account, address, proxy)
                    return reconnect_time
                else:
                    retry_count += 1
                    if retry_count < self.retry:
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address):<1} Attempt {retry_count} failed. Retrying...")
                        await asyncio.sleep(5)

            logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address):<1} Failed to get data.", log_type="error")
            return 86400

    async def process_accounts_with_semaphore(self, index: int, account: str, use_proxy: bool, semaphore):
        async with semaphore:
            return await self.process_accounts(index, account, use_proxy)
        
    async def register_from_file(self, use_proxy):
        if not os.path.exists(self.regist_file):
            logging("register.txt not found.", log_type="error")
            return

        with open(self.regist_file, 'r') as file:
            accounts = [line.strip() for line in file.readlines() if line.strip()]

        if not accounts:
            logging("No accounts found in register.txt", log_type="error")
            return

        for idx, account in enumerate(accounts, start=1):
            success = await self.process_registration(idx, account, use_proxy)
            if success:
                continue

    async def main(self):
        try:
            if not os.path.exists(self.account_file):
                logging(f"File '{self.account_file}' Not Found.")
                return

            accounts = self.wallet_manager.load_accounts()
            use_proxy_choice, num_wallets = await self.d3d_menu(accounts)
            use_proxy = use_proxy_choice in [1, 3, 5]

            if use_proxy:
                await self.proxy_manager.load_proxies()

            if use_proxy_choice in [5, 6]:
                wallets = self.wallet_manager.generate_wallets(num_wallets)
                if wallets:
                    with open(self.regist_file, 'a') as file:
                        for private_key, address in wallets:
                            file.write(f"{private_key}\n")
                            logging(f"Private key for {masked(address)} saved to regist_file.", log_type="success")

                    for idx, (private_key, _) in enumerate(wallets, start=1):
                        await self.process_registration(idx, private_key, use_proxy)
                return
            
            if use_proxy_choice in [3, 4] :
                await self.register_from_file(use_proxy)
                return  
                  
            semaphore = asyncio.Semaphore(self.MAX_THREADS)

            while True:
                tasks = []
                for idx, account in enumerate(accounts, start=1):
                    if account:
                        task = self.process_accounts_with_semaphore(idx, account, use_proxy, semaphore)
                        tasks.append(task)

                reconnect_times = await asyncio.gather(*tasks)
                delay = min(reconnect_times) if reconnect_times else 86400
                logging(f"Calculating wait time, please wait.... ", log_type="info")
                await X9A2B(self.account_file)._RUN()
                while delay > 0:
                    formatted_time = time_remain(delay)
                    logging(f"Waiting for {formatted_time}, All accounts have been processed.",log_type="success", end="\r", flush=True)
                    await asyncio.sleep(1)
                    delay -= 1

        except Exception as e:
            logging(f"An error occurred: {e}")
            e_logs(f"{e}")

from eth_account import Account
from utils.logger import logging, e_logs

class WalletManager:
    def __init__(self, account_file):
        self.account_file = account_file

    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            return address
        except Exception as e:
            return None

    def generate_wallets(self, num_wallets):
        wallets = []
        for _ in range(num_wallets):
            try:
                account = Account.create()
                private_key = account.key.hex()
                address = account.address
                wallets.append((private_key, address))
            except Exception as e:
                logging(f"Error generating wallet: {str(e)}", log_type="error")
                e_logs(f"{e}")
                continue
        return wallets

    def load_accounts(self):
        try:
            with open(self.account_file, 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            return accounts
        except Exception as e:
            logging(f"Error loading accounts: {str(e)}", log_type="error")
            e_logs(f"{e}")
            return []
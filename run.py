import sys, argparse
import asyncio
from config.config import ACCOUNT_FILE
from bot.core import LayerEdge
from utils.logger import logging

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LayerEdge Bot with a specific account file.")
    parser.add_argument("--run", type=str, default=ACCOUNT_FILE, help="Specify the account file to use.")
    args = parser.parse_args()

    try:
        bot = LayerEdge(args.run) 
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        logging(f"Keyboard interrupted by you", log_type="warning")
        sys.exit(0)


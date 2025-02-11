import asyncio, time
from utils.colors import *
from utils.utils import time_remain, masked
from utils.logger import logging

class NodeManager:
    def __init__(self, api_client, proxy_manager):
        self.api_client = api_client
        self.proxy_manager = proxy_manager

    async def handle_node_reconnection(self, index: int, account: str, address: str, proxy=None):
        reconnect_time = float('inf')

        node = await self.api_client.node_status(index, address, proxy)
        if node and node.get("message") == "node status":
            last_connect = node['data']['startTimestamp']

            if last_connect is None:
                start = await self.api_client.start_node(index, account, address, proxy)
                if start and start.get("message") == "node action executed successfully":
                    last_connect = start['data']['startTimestamp']
                    now_time = int(time.time())
                    reconnect_time = last_connect + 86400 - now_time
                    logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Connected until: {time_remain(reconnect_time)}", log_type="success")
            else:
                now_time = int(time.time())
                connect_time = last_connect + 86400

                if now_time >= connect_time:
                    stop = await self.api_client.stop_node(index, account, address, proxy)
                    if stop and stop.get("message") == "node action executed successfully":
                        logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Disconnected - Reconnecting...")
                        await asyncio.sleep(3)

                        start = await self.api_client.start_node(index, account, address, proxy)
                        if start and start.get("message") == "node action executed successfully":
                            last_connect = start['data']['startTimestamp']
                            now_time = int(time.time())
                            reconnect_time = last_connect + 86400 - now_time
                            logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Connected until: {time_remain(reconnect_time)}", log_type="success")
                else:
                    reconnect_time = connect_time - now_time
                    logging(f" {YELLOW}{index:<4}{RESET} | Address: {masked(address)} Already Connected until: {time_remain(reconnect_time)}")
        return reconnect_time
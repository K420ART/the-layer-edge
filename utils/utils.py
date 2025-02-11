import os
from bot.version import NAME, VERSION, COPYRIGHT 
from .colors import *

def ascii():
    ascii = r"""
 ██   ██ ██   ██ ██████   ██████  
 ██  ██  ██   ██      ██ ██  ████ 
 █████   ███████  █████  ██ ██ ██ 
 ██  ██       ██ ██      ████  ██ 
 ██   ██      ██ ███████  ██████  """ 
    print(Fore.BLUE + Style.BRIGHT + ascii + Style.RESET_ALL + f"{VERSION}")
    print(Fore.WHITE + Style.BRIGHT + f" {NAME}")
    print(Fore.WHITE + Style.BRIGHT + f" Copyright {Fore.WHITE + Style.BRIGHT}© {COPYRIGHT}")


def time_remain(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def masked(account):
    masked = account[:6] + '*' * 5 + account[-6:]
    return masked

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


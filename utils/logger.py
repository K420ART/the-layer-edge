from utils.colors import *
from datetime import datetime

log_mess = None

def logging(message, log_type="info", **kwargs):
    global log_mess
    log_types = {
        "info": (f"{BLUE}INFO{RESET}", BLACK),
        "success": (f"{GREEN}SUCCESS{RESET}", BLACK),
        "warning": (f"{YELLOW}WARNING{RESET}", BLACK),
        "error": (f"{RED}ERROR{RESET}", BLACK),
        "-": (f"{BLACK}       {RESET}", BLACK),
    }
    prefix, color = log_types.get(log_type.lower(), (f"{BLUE}INFO{RESET}", BLACK))
    time_now = datetime.now().strftime("%H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    padded = prefix.ljust(16) 
    if message != log_mess:
        print(BLACK + f"{time_now} | {padded} | {message}", flush=flush, end=end)
        log_mess = message

def e_logs(message):
    with open('logs/report.log', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {message}\n")
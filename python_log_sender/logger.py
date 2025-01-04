from colorama import Fore, Style, init
from datetime import datetime
from GoogleScripsLogger.python_log_sender.secrets import get_logger_url, get_rl_spreadsheet_id
import requests
import threading
from enum import Enum

# Initialize colorama
init()

class TerminalColors(Enum):
    WARNING = Fore.YELLOW
    ENDC = Style.RESET_ALL
    INFO = Fore.CYAN
    PENALTY = Fore.MAGENTA
    FAIL = Fore.RED
    STANDARD = Fore.WHITE
    

def send_log_to_spreadsheet(url, payload):
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        print(f"{TerminalColors.FAIL.value}Failed to send log to spreadsheet: {r.status_code}{TerminalColors.ENDC.value}")
    elif r.text == "Spread sheet id is not set":
            print(f"{TerminalColors.FAIL.value}Spread sheet id is not set{TerminalColors.ENDC.value}")
        

def log(text, color: TerminalColors = TerminalColors.STANDARD, log_file="log.txt"):
    """Logs a message to the console, file, and remote logger."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    print(f"{timestamp} - {color.value}{text}{TerminalColors.ENDC.value}")
    
    # Append the message to the log file
    try:
        with open(log_file, "a") as file:
            file.write(f"{timestamp} - {text}\n")
    except Exception as e:
        print(f"{TerminalColors.FAIL.value}Error writing to log file: {e}{TerminalColors.ENDC.value}")
    
    # Send the message to the logger URL asynchronously
    payload = {
        "timestamp": timestamp,
        "logLevel": color.name,
        "message": text,
        "spread_sheet_id": get_rl_spreadsheet_id()
    }
    threading.Thread(target=send_log_to_spreadsheet, args=(get_logger_url(), payload)).start()
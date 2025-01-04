from colorama import Fore, Style, init
from datetime import datetime
from python_log_sender.secrets import get_logger_url
import requests
# Initialize colorama
init()

class TerminalColors:
    WARNING = Fore.YELLOW
    ENDC = Style.RESET_ALL
    INFO = Fore.CYAN
    PENALTY = Fore.MAGENTA
    FAIL = Fore.RED
    STANDARD = Fore.WHITE
    
log_file = "log.txt"

def log(text, color:TerminalColors = TerminalColors.STANDARD):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    print(f"{timestamp} - {color}{text}{TerminalColors.ENDC}")
    # Append the message to the log file
    try:
        with open(log_file, "a") as file:
            file.write(f"{timestamp} - {text}\n")
    except Exception as e:
        print(f"{TerminalColors.FAIL}Error writing to log file: {e}{TerminalColors.ENDC}")
    # Send the message to the logger URL
    try:
        requests.post(get_logger_url(), json={
            "timestamp": timestamp, 
            "logLevel": color, 
            "message": text
            })
    except Exception as e:
        print(f"{TerminalColors.FAIL}Error sending message to logger: {e}{TerminalColors.ENDC}")

from colorama import Fore, Style, init
from datetime import datetime
from python_log_sender.secrets import get_logger_url
import httpx
import asyncio

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

async def send_log_async(url, payload):
    """Asynchronous helper to send log data."""
    async with httpx.AsyncClient() as client:
        # send and forget
        client.post(url, json=payload)

def log(text, color: TerminalColors = TerminalColors.STANDARD):
    """Logs a message to the console, file, and remote logger."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    print(f"{timestamp} - {color}{text}{TerminalColors.ENDC}")
    
    # Append the message to the log file
    try:
        with open(log_file, "a") as file:
            file.write(f"{timestamp} - {text}\n")
    except Exception as e:
        print(f"{TerminalColors.FAIL}Error writing to log file: {e}{TerminalColors.ENDC}")
    
    # Send the message to the logger URL asynchronously
    payload = {
        "timestamp": timestamp,
        "logLevel": color,
        "message": text
    }
    asyncio.run(send_log_async(get_logger_url(), payload))
import pyautogui
import sys
import time
import os
import json
import requests
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def tprint(message): # console print with timestamp
    timestamp = datetime.now().strftime("[%Y-%m-%d_%H:%M:%S]")
    print(f"{timestamp} {message}")

def send_screenshot():
    screenshot = pyautogui.screenshot()
    
    # Save to memory instead of disk
    img_buffer = BytesIO()
    screenshot.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    embed = {
        "title": "stupid screenshot bot",
        "color": 16711680, # #FF0000 in decimal
        "image": {
            "url": "attachment://screenshot.png"
        },
        "footer": {
            "text": "brought to you by arle.",
            "icon_url": "https://i.imgur.com/JdlwG9w.jpeg"
        }
    }
    
    payload = {"embeds": [embed]}
    files = {"file": ("screenshot.png", img_buffer, "image/png")}
    response = requests.post(WEBHOOK_URL, data={"payload_json": json.dumps(payload)}, files=files)
    
    if response.status_code != 200:
        tprint(f"Failed to send screenshot. Status code: {response.status_code}")

def get_next_send_time():
    now = datetime.now()
    return (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

def delete_last_line():
    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')

def main():
    try:
        hours_uptime = 0
        tprint("Sending initial screenshot...")
        delete_last_line()
        
        while True:
            send_screenshot()
            hours_uptime += 1

            next_time = get_next_send_time()
            sleep_seconds = (next_time - datetime.now()).total_seconds()
            
            tprint(f"Next screenshot at {next_time.strftime('%H:%M:%S')}")
            days = hours_uptime // 24
            hours = hours_uptime % 24
            tprint(f"Uptime: {days}d {hours}h")
            time.sleep(sleep_seconds)

            delete_last_line()
            delete_last_line()
    except KeyboardInterrupt:
        tprint("Shutting down gracefully... Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()
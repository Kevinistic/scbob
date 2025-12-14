import pyautogui
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
    
    if response.status_code == 200:
        tprint("Screenshot sent successfully")
    else:
        tprint(f"Failed to send screenshot. Status code: {response.status_code}")

def get_next_send_time():
    now = datetime.now()
    current_minute = now.minute
    
    # Determine next send time (either :00 or :30)
    if current_minute < 30:
        next_time = now.replace(minute=30, second=0, microsecond=0)
    else:
        # Go to next hour at :00
        next_time = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    
    return next_time

def main():
    try:
        tprint("Sending initial screenshot...")
        send_screenshot()
        
        while True:
            next_time = get_next_send_time()
            sleep_seconds = (next_time - datetime.now()).total_seconds()
            
            tprint(f"Next screenshot at {next_time.strftime('%H:%M:%S')} (in {sleep_seconds:.0f} seconds)")
            time.sleep(sleep_seconds)
            
            send_screenshot()
    except KeyboardInterrupt:
        tprint("Shutting down gracefully... Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()
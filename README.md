# screen capture thingamabob (scbob)

this thing automatically captures your entire screen and sends it to Discord via webhook at scheduled intervals. program is on release and considered done, no future updates will be made.

## features

- captures screenshots every hour
- sends an initial screenshot immediately on launch
- uploads screenshots directly to Discord embeds (no local file saved)
- timestamped console output with format `[YYYY-MM-DD_HH:MM:SS]`
- customizable Discord embed appearance

## requirements

- python 3.7+
- discord webhook URL

## Installation

1. clone or download this repository

2. install dependencies:
```bash
pip install -r requirements.txt
```

3. create a `.env` file in the same directory as `main.py`:
```env
WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE
```

## usage

run the script:
```bash
python main.py
```

the bot will:
1. send an initial screenshot immediately
2. wait until the next scheduled time (:00 in this case)
3. continue sending screenshots every 30 minutes

press `Ctrl+C` to stop the bot.

## how It Works

- screenshots are captured using `pyautogui`
- images are stored in memory (not saved to disk)
- timing is synchronized
- all activity is printed to console with timestamps

## license

See [LICENSE](LICENSE) file for details.

## credits
- @cn3z on Discord: everything lol
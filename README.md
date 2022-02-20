# ScreenTimeCLI

A command line tool that reads your Mac's screen time database and shows 
you exactly how you spend your time on your computer.

Built this because I wanted to see my actual usage data without going 
through System Settings every time.

## What it does

- Reads directly from Mac's screen time database
- Shows top apps by total usage time
- Daily screen time chart over the past 7 days
- Screen time broken down by hour of day
- Screen time by day of week
- Summary report with daily average and most used apps

## Requirements

- Python 3.x
- matplotlib
- colorama
- Mac with Screen Time enabled
- Terminal must have Full Disk Access enabled

## Setup
```bash
git clone https://github.com/yourusername/screentime-cli
cd screentime-cli
python3 -m venv venv
source venv/bin/activate
pip install matplotlib colorama
```

## Enable Full Disk Access

System Settings > Privacy & Security > Full Disk Access > add Terminal

## Usage
```bash
python3 screentime.py
```

## What I learned

- Reading SQLite databases with Python's sqlite3 module
- Apple's timestamp format (seconds since 2001-01-01)
- SQL queries - SELECT, WHERE, ORDER BY
- defaultdict for cleaner data aggregation
- Color coding charts based on data values
- Reading protected system files on Mac
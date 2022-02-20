from collections import defaultdict


def clean_app_name(app):
    # app names come as bundle ids like com.apple.Safari
    # extract just the last part
    if "." in app:
        parts = app.split(".")
        name = parts[-1]
    else:
        name = app

    # clean up common ones
    replacements = {
        "Safari": "Safari",
        "Code": "VS Code",
        "Terminal": "Terminal",
        "Finder": "Finder",
        "Music": "Music",
        "Messages": "Messages",
        "Mail": "Mail",
        "Notes": "Notes",
        "Photos": "Photos",
        "Slack": "Slack",
        "zoom.us": "Zoom",
        "figma": "Figma",
        "chrome": "Chrome",
        "firefox": "Firefox",
    }

    for key, value in replacements.items():
        if key.lower() in name.lower():
            return value

    return name.capitalize()


def get_app_totals(entries):
    totals = defaultdict(float)

    for entry in entries:
        app = clean_app_name(entry["app"])
        totals[app] += entry["duration_seconds"]

    # sort by most used
    sorted_totals = dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))
    return sorted_totals


def get_daily_totals(entries):
    daily = defaultdict(float)

    for entry in entries:
        daily[entry["date"]] += entry["duration_seconds"]

    return dict(sorted(daily.items()))


def get_hourly_totals(entries):
    hourly = defaultdict(float)

    for entry in entries:
        hourly[entry["hour"]] += entry["duration_seconds"]

    # fill missing hours with 0
    result = {}
    for hour in range(24):
        result[hour] = hourly.get(hour, 0)

    return result


def get_day_of_week_totals(entries):
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_totals = defaultdict(float)

    for entry in entries:
        day_totals[entry["day"]] += entry["duration_seconds"]

    result = {}
    for day in days_order:
        if day in day_totals:
            result[day] = day_totals[day]

    return result


def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    if hours > 0:
        return str(hours) + "h " + str(minutes) + "m"
    else:
        return str(minutes) + "m"


def get_most_productive_day(daily_totals):
    if not daily_totals:
        return None
    return min(daily_totals.items(), key=lambda x: x[1])


def get_most_wasted_day(daily_totals):
    if not daily_totals:
        return None
    return max(daily_totals.items(), key=lambda x: x[1])
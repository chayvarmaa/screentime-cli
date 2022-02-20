import sys
from colorama import init, Fore
from reader import fetch_usage_data, parse_rows
from analyzer import (
    get_app_totals,
    get_daily_totals,
    get_hourly_totals,
    get_day_of_week_totals,
    format_duration,
    get_most_productive_day,
    get_most_wasted_day
)
from visualizer import show_top_apps, show_daily_usage, show_hourly_usage, show_day_of_week

init(autoreset=True)


def print_banner():
    print("=" * 55)
    print("  ScreenTimeCLI - Mac screen time analyzer")
    print("=" * 55)


def print_menu():
    print("\nwhat do you want to see?")
    print("  1. top apps by usage")
    print("  2. daily screen time chart")
    print("  3. screen time by hour of day")
    print("  4. screen time by day of week")
    print("  5. summary report")
    print("  q. quit")
    print("")


def print_summary(entries, app_totals, daily_totals):
    total_seconds = sum(e["duration_seconds"] for e in entries)
    days = len(daily_totals)
    avg_seconds = total_seconds / days if days > 0 else 0

    most_used_app = list(app_totals.keys())[0] if app_totals else "n/a"
    most_used_time = list(app_totals.values())[0] if app_totals else 0

    best_day = get_most_productive_day(daily_totals)
    worst_day = get_most_wasted_day(daily_totals)

    print("\n" + "=" * 55)
    print("  summary - last 7 days")
    print("=" * 55)
    print("  total screen time : " + format_duration(total_seconds))
    print("  daily average     : " + format_duration(avg_seconds))
    print("  most used app     : " + most_used_app + " (" + format_duration(most_used_time) + ")")

    if best_day:
        print("  lightest day      : " + best_day[0] + " (" + format_duration(best_day[1]) + ")")
    if worst_day:
        print("  heaviest day      : " + worst_day[0] + " (" + format_duration(worst_day[1]) + ")")

    print("\n  top 5 apps:")
    for i, (app, seconds) in enumerate(list(app_totals.items())[:5], 1):
        bar = "#" * int(seconds / 3600)
        print("  " + str(i) + ". " + app.ljust(20) + format_duration(seconds).rjust(8) + "  " + bar)

    print("=" * 55)


def run():
    print_banner()
    print("\nloading screen time data...")

    rows, error = fetch_usage_data(days=7)

    if error:
        print(Fore.RED + "\nerror: " + error)
        sys.exit(1)

    if not rows:
        print(Fore.YELLOW + "\nno screen time data found for the last 7 days.")
        sys.exit(0)

    entries = parse_rows(rows)
    app_totals = get_app_totals(entries)
    daily_totals = get_daily_totals(entries)
    hourly_totals = get_hourly_totals(entries)
    day_totals = get_day_of_week_totals(entries)

    print("loaded " + str(len(entries)) + " usage records.\n")

    while True:
        print_menu()
        print("enter choice: ", end="", flush=True)
        choice = __import__('sys').stdin.readline().strip()

        if choice == "1":
            show_top_apps(app_totals)
        elif choice == "2":
            show_daily_usage(daily_totals)
        elif choice == "3":
            show_hourly_usage(hourly_totals)
        elif choice == "4":
            show_day_of_week(day_totals)
        elif choice == "5":
            print_summary(entries, app_totals, daily_totals)
        elif choice == "q":
            print("goodbye.")
            sys.exit(0)
        else:
            print("invalid choice.")


if __name__ == "__main__":
    run()
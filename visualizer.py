import matplotlib.pyplot as plt
from analyzer import format_duration


def show_top_apps(app_totals, limit=10):
    top = dict(list(app_totals.items())[:limit])

    apps = list(top.keys())
    seconds = list(top.values())
    hours = [round(s / 3600, 2) for s in seconds]

    colors = ["#e74c3c" if h > 4 else "#e67e22" if h > 2 else "#2ecc71" for h in hours]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(apps[::-1], hours[::-1], color=colors[::-1])
    plt.xlabel("hours")
    plt.title("top apps by screen time")

    # add time labels on bars
    for bar, hour, sec in zip(bars, hours[::-1], seconds[::-1]):
        plt.text(
            bar.get_width() + 0.05,
            bar.get_y() + bar.get_height() / 2,
            format_duration(sec),
            va="center",
            fontsize=9
        )

    plt.tight_layout()
    plt.show()


def show_daily_usage(daily_totals):
    dates = list(daily_totals.keys())
    hours = [round(s / 3600, 2) for s in daily_totals.values()]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, hours, marker="o", color="#3498db", linewidth=2)
    plt.fill_between(dates, hours, alpha=0.1, color="#3498db")
    plt.title("daily screen time")
    plt.xlabel("date")
    plt.ylabel("hours")
    plt.xticks(rotation=45)
    plt.axhline(y=sum(hours) / len(hours), color="red", linestyle="--", linewidth=0.8, label="average")
    plt.legend()
    plt.tight_layout()
    plt.show()


def show_hourly_usage(hourly_totals):
    hours = list(hourly_totals.keys())
    minutes = [round(s / 60, 1) for s in hourly_totals.values()]

    plt.figure(figsize=(12, 5))
    plt.bar(hours, minutes, color="#9b59b6")
    plt.title("screen time by hour of day")
    plt.xlabel("hour (24h)")
    plt.ylabel("minutes")
    plt.xticks(hours)
    plt.tight_layout()
    plt.show()


def show_day_of_week(day_totals):
    days = list(day_totals.keys())
    hours = [round(s / 3600, 2) for s in day_totals.values()]

    plt.figure(figsize=(9, 5))
    plt.bar(days, hours, color="#1abc9c")
    plt.title("screen time by day of week")
    plt.xlabel("day")
    plt.ylabel("hours")
    plt.tight_layout()
    plt.show()
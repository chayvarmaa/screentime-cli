import sqlite3
import os
import glob
from datetime import datetime, timedelta


def get_database_path():
    # Mac stores screen time data here
    base = os.path.expanduser("~")
    pattern = base + "/Library/Application Support/Knowledge/knowledgeC.db"
    
    if os.path.exists(pattern):
        return pattern
    
    # try alternate location
    alt = "/private/var/db/CoreDuet/Knowledge/knowledgeC.db"
    if os.path.exists(alt):
        return alt

    return None


def fetch_usage_data(days=7):
    db_path = get_database_path()

    if not db_path:
        return None, "screen time database not found. make sure Full Disk Access is enabled."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # convert to apple's timestamp format (seconds since 2001-01-01)
        apple_epoch = datetime(2001, 1, 1)
        start_ts = (start_date - apple_epoch).total_seconds()
        end_ts = (end_date - apple_epoch).total_seconds()

        query = """
            SELECT
                ZOBJECT.ZVALUESTRING as app,
                ZOBJECT.ZSTARTDATE as start_date,
                ZOBJECT.ZENDDATE as end_date,
                (ZOBJECT.ZENDDATE - ZOBJECT.ZSTARTDATE) as duration
            FROM ZOBJECT
            WHERE ZOBJECT.ZSTREAMNAME = '/app/usage'
            AND ZOBJECT.ZSTARTDATE > ?
            AND ZOBJECT.ZENDDATE < ?
            AND ZOBJECT.ZVALUESTRING IS NOT NULL
            AND (ZOBJECT.ZENDDATE - ZOBJECT.ZSTARTDATE) > 0
            ORDER BY ZOBJECT.ZSTARTDATE ASC
        """

        cursor.execute(query, (start_ts, end_ts))
        rows = cursor.fetchall()
        conn.close()

        return rows, None

    except sqlite3.OperationalError as e:
        return None, "could not read database: " + str(e) + "\nTry enabling Full Disk Access for Terminal."
    except Exception as e:
        return None, "unexpected error: " + str(e)


def parse_rows(rows):
    apple_epoch = datetime(2001, 1, 1)
    entries = []

    for row in rows:
        app, start_ts, end_ts, duration = row

        start_dt = apple_epoch + timedelta(seconds=start_ts)
        end_dt = apple_epoch + timedelta(seconds=end_ts)

        entries.append({
            "app": app,
            "start": start_dt,
            "end": end_dt,
            "duration_seconds": duration,
            "date": start_dt.strftime("%Y-%m-%d"),
            "day": start_dt.strftime("%A"),
            "hour": start_dt.hour
        })

    return entries
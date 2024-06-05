import time
import sqlite3
from datetime import datetime, timedelta
import platform
from AppKit import NSWorkspace
import subprocess

def get_active_window():
    return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

def log_time(window_title, start_time, end_time):
    conn = sqlite3.connect('time_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_log (
            id INTEGER PRIMARY KEY,
            window_title TEXT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER
        )
    ''')
    duration = int((end_time - start_time).total_seconds())
    cursor.execute('''
        INSERT INTO time_log (window_title, start_time, end_time, duration)
        VALUES (?, ?, ?, ?)
    ''', (window_title, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
    conn.commit()
    conn.close()

def generate_daily_summary():
    conn = sqlite3.connect('time_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT window_title, SUM(duration) as total_duration
        FROM time_log
        WHERE start_time >= date('now', 'start of day')
        GROUP BY window_title
        ORDER BY total_duration DESC
    ''')
    rows = cursor.fetchall()
    summary = "\n".join([f"{row[0]}: {timedelta(seconds=row[1])}" for row in rows])
    print("Daily Summary")
    print(summary)
    conn.close()

def is_charging():
    result = subprocess.Popen(['pmset', '-g', 'batt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = result.communicate()
    return "AC Power" in output.decode('utf-8')

def main():
    last_window = None
    start_time = None
    last_summary_time = datetime.now()

    while True:
        if not is_charging():
            print("Not connected to a power source. Pausing tracking.")
            time.sleep(60)  # Wait for 1 minute before checking again
            continue

        current_window = get_active_window()
        if current_window and current_window != last_window:
            end_time = datetime.now()
            if last_window:
                log_time(last_window, start_time, end_time)
            last_window = current_window
            start_time = datetime.now()

        # Generate daily summary at a specific time (e.g., at midnight)
        if datetime.now().hour == 0 and (datetime.now() - last_summary_time).days > 0:
            generate_daily_summary()
            last_summary_time = datetime.now()

        time.sleep(5)  # Check every 5 seconds

if __name__ == '__main__':
    main()
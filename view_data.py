import sqlite3
from datetime import timedelta

def view_data():
    conn = sqlite3.connect('time_tracking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT window_title, start_time, end_time, duration FROM time_log ORDER BY start_time DESC')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        print(f"Window: {row[0]}")
        print(f"Start: {row[1]}")
        print(f"End: {row[2]}")
        print(f"Duration: {timedelta(seconds=row[3])}")
        print()

if __name__ == '__main__':
    view_data()
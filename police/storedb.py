import sqlite3
import random
from datetime import datetime, timedelta

# Sample known localities in Coimbatore with lat/lon
locations = [
    ("Gandhipuram", 11.0174, 76.9662),
    ("Peelamedu", 11.0300, 77.0000),
    ("Saravanampatti", 11.0737, 76.9981),
    ("RS Puram", 11.0056, 76.9551),
    ("Kallapatti", 11.0514, 77.0386),
    ("Singanallur", 11.0082, 77.0343),
    ("Town Hall", 11.0086, 76.9616),
    ("Saibaba Colony", 11.0180, 76.9440),
    ("Ukkadam", 10.9975, 76.9610),
    ("Vadavalli", 11.0237, 76.8998),
    ("Race Course", 11.0088, 76.9705),
    ("Thudiyalur", 11.0718, 76.9511)
]

# Create or connect to the SQLite database
conn = sqlite3.connect("gps_data.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS gps_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    datetime TEXT,
    location TEXT
)
''')

# Generate and insert 144 data points (10 min interval)
start_datetime = datetime(2024, 1, 1, 8, 0, 0)
for i in range(144):
    loc_name, base_lat, base_lon = random.choice(locations)
    lat = round(base_lat + random.uniform(-0.001, 0.001), 6)
    lon = round(base_lon + random.uniform(-0.001, 0.001), 6)
    timestamp = start_datetime + timedelta(minutes=10 * i)
    datetime_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO gps_data (latitude, longitude, datetime, location) VALUES (?, ?, ?, ?)",
                   (lat, lon, datetime_str, loc_name))

conn.commit()
conn.close()

"gps_data.db"

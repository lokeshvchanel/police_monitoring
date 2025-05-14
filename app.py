from flask import Flask, render_template, send_file
import sqlite3
import csv
import io

app = Flask(__name__)
DB_PATH = 'gps_data.db'

# Hardcoded data (keep this in sync with index.html)
HARDCODED_CALL_LOGS = [
    ("+919876543210", "2024-09-10 09:15", "02:15", "Incoming"),
    ("+918123456789", "2024-09-10 10:20", "01:05", "Outgoing"),
    ("+917123456789", "2024-09-10 11:30", "00:00", "Missed"),
    ("+919888888888", "2024-09-10 12:45", "03:10", "Incoming"),
    ("+917654321234", "2024-09-10 14:05", "00:55", "Outgoing"),
    ("+918976543210", "2024-09-10 15:25", "00:00", "Missed"),
    ("+919123456789", "2024-09-10 16:40", "04:20", "Incoming"),
    ("+917777777777", "2024-09-10 17:50", "00:35", "Outgoing"),
    ("+918765432109", "2024-09-10 18:15", "01:45", "Incoming"),
    ("+916543210987", "2024-09-10 19:05", "00:00", "Missed"),
    ("+919876541234", "2024-09-10 20:25", "02:00", "Outgoing"),
    ("+918123498765", "2024-09-10 21:35", "01:20", "Incoming"),
    ("+917654312345", "2024-09-10 22:40", "03:05", "Outgoing"),
    ("+919123409876", "2024-09-10 23:50", "00:00", "Missed"),
    ("+917001122334", "2024-09-11 00:10", "00:50", "Incoming")
]
HARDCODED_RESPONSE_LOGS = [
    ("+919876543210", "2024-09-10 09:15", "Unsolved"),
    ("+918123456789", "2024-09-10 10:20", "Solved"),
    ("+917123456789", "2024-09-10 11:30", "Unsolved"),
    ("+919888888888", "2024-09-10 12:45", "Solved"),
    ("+917654321234", "2024-09-10 14:05", "Solved"),
    ("+918976543210", "2024-09-10 15:25", "Unsolved"),
    ("+919123456789", "2024-09-10 16:40", "Solved"),
    ("+917777777777", "2024-09-10 17:50", "Solved"),
    ("+918765432109", "2024-09-10 18:15", "Unsolved"),
    ("+916543210987", "2024-09-10 19:05", "Unsolved"),
    ("+919876541234", "2024-09-10 20:25", "Solved"),
    ("+918123498765", "2024-09-10 21:35", "Solved"),
    ("+917654312345", "2024-09-10 22:40", "Unsolved"),
    ("+919123409876", "2024-09-10 23:50", "Unsolved"),
    ("+917001122334", "2024-09-11 00:10", "Solved")
]

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT latitude, longitude, datetime, location FROM gps_data ORDER BY datetime DESC")
    gps_data = cursor.fetchall()

    conn.close()
    return render_template('index.html',
                           gps_data=gps_data,
                           call_logs=HARDCODED_CALL_LOGS,
                           response_logs=HARDCODED_RESPONSE_LOGS)

@app.route('/download')
def download_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude, datetime, location FROM gps_data ORDER BY datetime DESC")
    gps_data = cursor.fetchall()
    conn.close()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # GPS Data
    writer.writerow(['--- Beat Officer Saravanan ---'])
    writer.writerow(['Latitude', 'Longitude', 'Datetime', 'Location'])
    writer.writerows(gps_data)

    # Call Logs
    writer.writerow([])
    writer.writerow(['--- Call Logs of Officer saravanan ---'])
    writer.writerow(['Phone Number', 'Datetime', 'Duration', 'Type'])
    writer.writerows(HARDCODED_CALL_LOGS)

    # Response Logs
    writer.writerow([])
    writer.writerow(['---  Response Logs of Officer saravanan ---'])
    writer.writerow(['Phone Number', 'Datetime', 'Status'])
    writer.writerows(HARDCODED_RESPONSE_LOGS)

    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='all_data.csv')

if __name__ == '__main__':
    app.run(debug=True)

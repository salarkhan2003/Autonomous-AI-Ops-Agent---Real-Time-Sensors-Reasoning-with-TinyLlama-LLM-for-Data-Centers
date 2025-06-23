import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "sensors.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (timestamp TEXT, rack_id INTEGER, temp REAL, humidity REAL, voltage REAL, current REAL, pressure REAL)''')
    conn.commit()
    conn.close()

def store_data(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?, ?, ?)",
              (data["timestamp"], data["rack_id"], data["temp"], data["humidity"], data["voltage"], data["current"], data["pressure"]))
    conn.commit()
    conn.close()

def get_recent_data(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return [{"timestamp": d[0], "rack_id": d[1], "temp": d[2], "humidity": d[3], "voltage": d[4], "current": d[5], "pressure": d[6]} for d in data]
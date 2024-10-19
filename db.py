import sqlite3
import json
from datetime import date, time, datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, time)):
            return obj.isoformat()
        return super().default(obj)


class VibecheckDB:
    def __init__(self):
        self.db_name = "vibecheck.db"
        self.conn = sqlite3.connect(self.db_name)
        self.initialize_database()

    def initialize_database(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS artist_mapping (
            ra_artist_id TEXT PRIMARY KEY,
            spotify_artist_id TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY,
            event_data TEXT
        )
        """)
        self.conn.commit()

    def save_event(self, event_info):
        cursor = self.conn.cursor()
        event_data = json.dumps(event_info, cls=DateTimeEncoder)
        cursor.execute(
            "INSERT OR REPLACE INTO events (event_id, event_data) VALUES (?, ?)",
            (event_info["id"], event_data),
        )
        self.conn.commit()

    def get_event(self, event_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT event_data FROM events WHERE event_id = ?", (event_id,))
        result = cursor.fetchone()
        if result:
            event_data = json.loads(result[0], object_hook=self._datetime_decoder)
            return event_data
        return None

    @staticmethod
    def _datetime_decoder(dct):
        for key, value in dct.items():
            if isinstance(value, str):
                try:
                    # Try parsing as datetime first
                    dct[key] = datetime.fromisoformat(value)
                except ValueError:
                    try:
                        # If that fails, try parsing as date
                        dct[key] = date.fromisoformat(value)
                    except ValueError:
                        try:
                            # If that fails, try parsing as time
                            dct[key] = time.fromisoformat(value)
                        except ValueError:
                            # If all parsing attempts fail, leave the value as is
                            pass
        return dct

    def get_spotify_artist_id(self, ra_artist_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT spotify_artist_id FROM artist_mapping WHERE ra_artist_id = ?",
            (ra_artist_id,),
        )
        result = cursor.fetchone()
        return result[0] if result else None

    def save_artist_mapping(self, ra_artist_id, spotify_artist_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO artist_mapping (ra_artist_id, spotify_artist_id) VALUES (?, ?)",
            (ra_artist_id, spotify_artist_id),
        )
        self.conn.commit()

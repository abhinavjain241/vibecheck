import sqlite3


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
        self.conn.commit()

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

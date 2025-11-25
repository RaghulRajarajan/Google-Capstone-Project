"""
MemoryBank: simple sqlite-based memory for meeting summaries and actions.
"""
import sqlite3
import json
import logging
logger = logging.getLogger("memory")

class MemoryBank:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS meetings (
                id TEXT PRIMARY KEY,
                transcript TEXT,
                summary TEXT,
                actions TEXT,
                issues TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_meeting(self, meeting_id, transcript, summary, actions, issues):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO meetings(id, transcript, summary, actions, issues)
            VALUES (?, ?, ?, ?, ?)
        """, (meeting_id, transcript, summary, json.dumps(actions), json.dumps(issues)))
        self.conn.commit()
        logger.info("Meeting %s saved to memory", meeting_id)

    def query_meetings(self, q):
        cur = self.conn.cursor()
        cur.execute("SELECT id, summary FROM meetings WHERE summary LIKE ? LIMIT 20", (f"%{q}%",))
        return cur.fetchall()

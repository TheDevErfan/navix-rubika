"""
Finite State Machine (FSM) with SQLite Persistent Storage for Navix
"""
import sqlite3
import json
from typing import Dict, Any
from .log import logger

class MemoryStorage:
    """
    حافظه موقت در رم (RAM)
    """
    def __init__(self):
        self._states: Dict[str, str] = {}
        self._data: Dict[str, Dict[str, Any]] = {}
        logger.debug("حافظه FSM موقت (MemoryStorage) راه‌اندازی شد.")

    async def set_state(self, user_id: str, state: str):
        self._states[str(user_id)] = state

    async def get_state(self, user_id: str) -> str:
        return self._states.get(str(user_id))

    async def set_data(self, user_id: str, data: dict):
        self._data[str(user_id)] = data

    async def get_data(self, user_id: str) -> dict:
        return self._data.get(str(user_id), {})


class SQLiteStorage:
    """
    حافظه دائمی و پایدار بر پایه دیتابیس SQLite برای FSM
    """
    def __init__(self, db_path: str = "navix_fsm.db"):
        self.db_path = db_path
        self._init_db()
        logger.debug(f"حافظه پایدار SQLite برای FSM در مسیر {db_path} راه‌اندازی شد.")

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fsm_states (
                    user_id TEXT PRIMARY KEY,
                    state TEXT,
                    data TEXT
                )
            """)
            conn.commit()

    async def set_state(self, user_id: str, state: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fsm_states (user_id, state, data) VALUES (?, ?, '{}')
                ON CONFLICT(user_id) DO UPDATE SET state=excluded.state
            """, (str(user_id), state))
            conn.commit()

    async def get_state(self, user_id: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT state FROM fsm_states WHERE user_id = ?", (str(user_id),))
            row = cursor.fetchone()
            return row[0] if row else None

    async def set_data(self, user_id: str, data: dict):
        data_json = json.dumps(data)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fsm_states (user_id, state, data) VALUES (?, NULL, ?)
                ON CONFLICT(user_id) DO UPDATE SET data=excluded.data
            """, (str(user_id), data_json))
            conn.commit()

    async def get_data(self, user_id: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM fsm_states WHERE user_id = ?", (str(user_id),))
            row = cursor.fetchone()
            if row and row[0]:
                try:
                    return json.loads(row[0])
                except Exception:
                    return {}
            return {}

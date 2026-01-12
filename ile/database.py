import os
import sqlite3
from pathlib import Path

SCHEMA_FILE = Path(__file__).with_name("schema.sql")
DB_PATH = Path("vera_data") / "experiences.db"


class VERADatabase:
    """SQLite database for VERA's ILE memory."""

    def __init__(self, db_path: Path | str = DB_PATH):
        """Initialize database connection."""
        self.db_path = Path(db_path)
        self.conn: sqlite3.Connection | None = None
        self._init_db()

    def _init_db(self):
        """Initialize database and load schema."""
        # Create vera_data directory if it doesn't exist
        os.makedirs(self.db_path.parent, exist_ok=True)
        
        # Connect to database
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Load and execute schema
        if SCHEMA_FILE.exists():
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema_sql = f.read()
                self.conn.executescript(schema_sql)
            self.conn.commit()
            print(f"[ILE] Database initialized: {self.db_path}")
        else:
            print(f"[ILE] WARNING: schema.sql not found at {SCHEMA_FILE}")
            print("[ILE] Database will be incomplete")

    def execute(self, query: str, params: tuple | None = None):
        """Execute query and commit."""
        if self.conn is None:
            raise RuntimeError("Database connection closed")
        
        cur = self.conn.cursor()
        cur.execute(query, params or ())
        self.conn.commit()
        return cur

    def fetch_all(self, query: str, params: tuple | None = None):
        """Fetch all rows from query."""
        if self.conn is None:
            raise RuntimeError("Database connection closed")
        
        cur = self.execute(query, params)
        return cur.fetchall()

    def fetch_one(self, query: str, params: tuple | None = None):
        """Fetch single row from query."""
        if self.conn is None:
            raise RuntimeError("Database connection closed")
        
        cur = self.execute(query, params)
        return cur.fetchone()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("[ILE] Database connection closed")

    def __del__(self):
        """Ensure connection closes on deletion."""
        self.close()

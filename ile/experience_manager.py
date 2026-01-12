"""
ile_experience_manager.py - FIXED VERSION
Handles storing and retrieving user interactions
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import uuid
import threading

class ExperienceManager:
    """Manages persistent memory of interactions"""
    
    def __init__(self, db_path: str = "vera_data/experiences.db"):
        """Initialize the experience manager"""
        self.db_path = db_path
        self.session_id = None
        self.connection = None
        self.lock = threading.Lock()
        
        # Create directory if needed
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        print(f"[ILE] Database initialized: {self.db_path}")
    
    def _init_database(self):
        """Initialize database with schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    interaction_count INTEGER DEFAULT 0,
                    user_name TEXT
                )
            ''')
            
            # Create experiences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_input TEXT,
                    vera_response TEXT,
                    response_length INTEGER,
                    confidence_score REAL,
                    vera_reflection TEXT,
                    domain TEXT,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                )
            ''')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ILE] Database init error: {e}")
            return False
    
    def start_session(self, user_name: str = "VERA_User"):
        """Start a new session"""
        try:
            self.session_id = str(uuid.uuid4())[:8]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sessions (id, start_time, user_name, interaction_count)
                VALUES (?, ?, ?, ?)
            ''', (self.session_id, datetime.now().isoformat(), user_name, 0))
            
            conn.commit()
            conn.close()
            
            print(f"[ILE] ✓ Session started: {self.session_id}")
            return self.session_id
        except Exception as e:
            print(f"[ILE] Session start error: {e}")
            return None
    
    def store_interaction(self, 
                         user_input: str,
                         vera_response: str,
                         confidence: float = 0.75,
                         reflection: str = "",
                         domain: Optional[str] = None) -> bool:
        """Store a single interaction in the database
        
        Args:
            user_input: User's input message
            vera_response: VERA's response
            confidence: Confidence score (0-1)
            reflection: VERA's reflection on the response
            domain: Domain/category of interaction
            
        Returns:
            True if stored successfully, False otherwise
        """
        if not self.session_id:
            print("[ILE] Error: No active session")
            return False
        
        try:
            # Use threading lock to prevent concurrent writes
            with self.lock:
                conn = sqlite3.connect(self.db_path, timeout=5.0)
                conn.isolation_level = None  # Autocommit mode
                cursor = conn.cursor()
                
                # Insert experience
                cursor.execute('''
                    INSERT INTO experiences 
                    (session_id, timestamp, user_input, vera_response, response_length, 
                     confidence_score, vera_reflection, domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id,
                    datetime.now().isoformat(),
                    user_input[:2000],  # Limit to 2000 chars
                    vera_response[:5000],  # Limit to 5000 chars
                    len(vera_response),
                    confidence,
                    reflection[:500],  # Limit to 500 chars
                    domain
                ))
                
                # Update session interaction count
                cursor.execute('''
                    UPDATE sessions 
                    SET interaction_count = interaction_count + 1
                    WHERE id = ?
                ''', (self.session_id,))
                
                conn.close()
                return True
                
        except sqlite3.OperationalError as e:
            print(f"[ILE] Database error (operational): {e}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"[ILE] Database error (integrity): {e}")
            return False
        except Exception as e:
            print(f"[ILE] Store error: {type(e).__name__}: {e}")
            return False
    
    def get_total_count(self) -> int:
        """Get total number of stored experiences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM experiences')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"[ILE] Count error: {e}")
            return 0
    
    def get_session_count(self) -> int:
        """Get interaction count for current session"""
        if not self.session_id:
            return 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT interaction_count FROM sessions WHERE id = ?', 
                         (self.session_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"[ILE] Session count error: {e}")
            return 0
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict]:
        """Get recent interactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM experiences
                ORDER BY id DESC
                LIMIT ?
            ''', (limit,))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            print(f"[ILE] Fetch error: {e}")
            return []
    
    def close(self):
        """Close session and cleanup"""
        if not self.session_id:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Mark session as ended
            cursor.execute('''
                UPDATE sessions
                SET end_time = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), self.session_id))
            
            conn.commit()
            conn.close()
            
            print(f"[ILE] Session ended: {self.session_id}")
        except Exception as e:
            print(f"[ILE] Close error: {e}")
        
        self.session_id = None
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()

-- V.E.R.A ILE Database Schema - Phase 1
-- Persistent memory foundation for VERA
-- Created: 2026-01-12

-- ============================================================================
-- SESSIONS: Track user sessions
-- ============================================================================

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    interaction_count INTEGER DEFAULT 0,
    user_name TEXT,
    session_notes TEXT
);

-- ============================================================================
-- EXPERIENCES: Every interaction VERA has
-- ============================================================================

CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Interaction content
    user_input TEXT NOT NULL,
    vera_response TEXT NOT NULL,
    response_length INTEGER,
    
    -- Quality metrics (Phase 1: basic)
    confidence_score REAL DEFAULT 0.5,
    
    -- Analysis (Phase 2+)
    vera_reflection TEXT,
    domain TEXT,
    
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0)
);

-- ============================================================================
-- INDICES: Performance optimization
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_experiences_session 
    ON experiences(session_id);

CREATE INDEX IF NOT EXISTS idx_experiences_timestamp 
    ON experiences(timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_experiences_domain 
    ON experiences(domain);

CREATE INDEX IF NOT EXISTS idx_sessions_start_time 
    ON sessions(start_time DESC);

# database.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()
    
    # Create table for user sessions
    c.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        native_language TEXT,
        learning_language TEXT,
        proficiency_level TEXT,
        start_time TIMESTAMP,
        end_time TIMESTAMP
    )
    ''')
    
    # Create table for user mistakes
    c.execute('''
    CREATE TABLE IF NOT EXISTS mistakes (
        id INTEGER PRIMARY KEY,
        session_id INTEGER,
        mistake_text TEXT,
        correction TEXT,
        mistake_type TEXT,
        timestamp TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES sessions (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def create_session(user_id, native_language, learning_language, proficiency_level):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT INTO sessions (user_id, native_language, learning_language, proficiency_level, start_time)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, native_language, learning_language, proficiency_level, datetime.now()))
    
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return session_id

def record_mistake(session_id, mistake_text, correction, mistake_type):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT INTO mistakes (session_id, mistake_text, correction, mistake_type, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (session_id, mistake_text, correction, mistake_type, datetime.now()))
    
    conn.commit()
    conn.close()

def get_session_mistakes(session_id):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()
    
    c.execute('SELECT mistake_text, correction, mistake_type FROM mistakes WHERE session_id = ?', (session_id,))
    mistakes = c.fetchall()
    
    conn.close()
    return mistakes

def end_session(session_id):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()
    
    c.execute('UPDATE sessions SET end_time = ? WHERE id = ?', (datetime.now(), session_id))
    
    conn.commit()
    conn.close()

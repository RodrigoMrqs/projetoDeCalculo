import sqlite3
import json

SCHEMA = '''
CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    area REAL,
    theta REAL,
    profits TEXT,
    best TEXT
);
'''

def init_db(db_path='projeto.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()

def save_scenario(db_path, payload: dict):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO scenarios(area, theta, profits, best) VALUES (?, ?, ?, ?)',
                (payload['area'], payload['theta'], json.dumps(payload['profits']), payload['best']))
    conn.commit()
    conn.close()

def load_scenarios(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT id, created_at, area, theta, profits, best FROM scenarios ORDER BY id DESC LIMIT 20')
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        res.append({'id': r[0], 'created_at': r[1], 'area': r[2], 'theta': r[3],
                    'profits': json.loads(r[4]), 'best': r[5]})
    return res

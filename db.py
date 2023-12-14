import sqlite3
from flask import Flask, g
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')
# Above is what determines the base directory
def get_db():
    """Open a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database with the schema."""
    db = get_db()
    with open(os.path.join(BASE_DIR, 'schema.sql'), 'r') as f:
        db.executescript(f.read())
    db.close()

def init_db_app_context():
    """Initialize the database within an app context for manual invocation."""
    with app.app_context():
        init_db()

if __name__ == '__main__':
    init_db_app_context()
    print("Database initialized.")
# When the script is directly it will initialize tha database
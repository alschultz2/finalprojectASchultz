import sqlite3
from flask import g
import os

# Set the path to your database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def get_db():
    """Open a new database connection if there is none yet for the
    current application context."""
    if 'db' not in g:
        # Connect to the database
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Use the sqlite3.Row type for rows. This allows accessing columns by name.
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database with the schema."""
    db = get_db()
    with open(os.path.join(BASE_DIR, 'schema.sql'), 'r') as f:
        db.executescript(f.read())
    db.close()

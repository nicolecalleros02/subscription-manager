import sqlite3

from flask import current_app, g

# Check if a database connection already exists in the application
def get_db():
    # If no database connection exists, create a new one
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Reads columns by name instead of index
        g.db.execute("PRAGMA foreign_keys = ON")  # Allows ON DELETE CASCADE to work
    return g.db


# Close the database connection when request ends
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Initialize the database with the schema
def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


# Register database functions with the Flask app
def init_app(app):
    app.teardown_appcontext(close_db)
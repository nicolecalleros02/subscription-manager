from app.db import get_db

# Add new user and return their id
def create_user(full_name, username, email, password_hash):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (full_name, username, email, password_hash) "
        "VALUES (?, ?, ?, ?)",
        (full_name, username, email.lower(), password_hash)
    )
    db.commit()
    return cursor.lastrowid


# Get user by id
def get_user_by_id(user_id):
    row = get_db().execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    return dict(row) if row else None


# Get user by email
def get_user_by_email(email):
    row = get_db().execute(
        "SELECT * FROM users WHERE email = ?", 
        (email.lower(),)
    ).fetchone()
    return dict(row) if row else None


# Get user by username
def get_user_by_username(username):
    row = get_db().execute(
        "SELECT * FROM users WHERE username = ?", 
        (username,)
    ).fetchone()
    return dict(row) if row else None


# Edit Account: change name and email
def update_user(user_id, full_name, email):
    db = get_db()
    db.execute(
        "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
        (full_name, email.lower(), user_id))
    db.commit()


# Edit Account: save new hashed password
def update_password(user_id, password_hash):
    db = get_db()
    db.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?", 
        (password_hash, user_id))
    db.commit()


# Settings: turn renewal reminders on or off
def update_notifications(user_id, enabled):
    db = get_db()
    db.execute(
        "UPDATE users SET notifications_enabled = ? WHERE id = ?",
        (int(enabled), user_id))
    db.commit()


# Delete Account: removes user (and their subscriptions automatically)
def delete_user(user_id):
    db = get_db()
    db.execute(
        "DELETE FROM users WHERE id = ?", 
        (user_id,))
    db.commit()

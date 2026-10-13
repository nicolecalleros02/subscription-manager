from flask import Blueprint

import sqlite3

from werkzeug.security import generate_password_hash

from app.db import get_db

import re

bp = Blueprint("auth", __name__, url_prefix="/auth")

def validate_registration(full_name, username, email, password):
    errors = {}

    if not full_name.strip():
        errors["full_name"] = "Full name is required."

    if not username.strip():
        errors["username"] = "Username is required."
    else:
        db = get_db()
        existing_user = db.execute(
            "SELECT id FROM users WHERE username = ?",
            (username.strip(),)
        ).fetchone()

        if existing_user:
            errors["username"] = "Username is already taken."

    if not email.strip():
        errors["email"] = "Email is required."
    elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        errors["email"] = "Please enter a valid email address."

    else:
        db = get_db()
        existing_email = db.execute(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(?)",
            (email.strip(),)
        ).fetchone()

        if existing_email:
            errors["email"] = "Email is already registered."

    if not password:
        errors["password"] = "Password is required."

    return errors
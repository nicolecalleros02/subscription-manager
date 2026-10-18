import sqlite3
import re

from flask import Blueprint, session, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash

from app.db import get_db

# Initialize blueprint for authentication routes
bp = Blueprint("auth", __name__, url_prefix="/auth")

# Validate registration input fields
def validate_registration(full_name, username, email, password):
    errors = {}

    # Check if field is empty
    if not full_name.strip():
        errors["full_name"] = "Full name is required."

    if not username.strip():
        errors["username"] = "Username is required."
    else:
        # Searches db for existing username
        db = get_db()
        existing_user = db.execute(
            "SELECT id FROM users WHERE username = ?",
            (username.strip(),)
        ).fetchone()

        if existing_user:
            errors["username"] = "Username is already taken."

    # Check and validate email format
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


# Validate login input fields
def validate_login(username, password):
    errors = {}

    # Check if username is missing or contains only whitespace
    if not username or not username.strip():
        errors["username"] = "Username is required."

    # Check if password is missing
    if not password:
        errors["password"] = "Password is required."

    return errors


# User registration
@bp.route("/registration", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        errors = validate_registration(full_name, username, email, password)

        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        # Insert new user into db
        if len(errors) == 0:
            db = get_db()
            try:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO users (full_name, username, email, password_hash) VALUES (?, ?, ?, ?)",
                    (full_name, username, email, password)
                )
                db.commit()
                
                # Log user in automatically with new db ID
                session.clear()
                session["user_id"] = cursor.lastrowid
                session.permanent = False   # Session will expire when the browser is closed
                
                return redirect(url_for("dashboard.index"))
                
            except sqlite3.IntegrityError:
                errors["database"] = "An error occurred while registering the user."

        return render_template("registration.html", errors=errors, full_name=full_name, username=username, email=email)

    return render_template("registration.html", errors={})


# User login
@bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        errors = validate_login(username, password)

        # Check for validation errors before querying db
        if len(errors) == 0:
            db = get_db()
            user = db.execute(
                "SELECT id, password_hash FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if user is None or user["password_hash"] != password:
                errors["login"] = "Invalid username or password."
            else:
                # Log user in
                session.clear()
                session["user_id"] = user["id"]
                session.permanent = False 

                return redirect(url_for("dashboard.index"))

        return render_template("login.html", errors=errors, username=username)

    return render_template("login.html", errors={})
    
import os
from datetime import datetime

from flask import Flask

from . import db


def create_app(test_config=None):
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)

    # Load settings from config.py
    app.config.from_object("config.Config")

    # Tests pass in own settings, which replaces defaults
    if test_config:
        app.config.update(test_config)

    # Make "instance" folder to hold database file
    os.makedirs(app.instance_path, exist_ok=True)

    # Where database file lives
    app.config.setdefault(
        "DATABASE", os.path.join(app.instance_path, "subscription_manager.db")
    )

    # Connect database code and create the tables
    db.init_app(app)
    with app.app_context():
        db.init_db()

    # Plug in each team member's pages
    from .routes import auth, dashboard, subscriptions

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(subscriptions.bp)

    # HTML show dates like "Nov 05, 2026" instead of "2026-11-05"
    @app.template_filter("fmt_date")
    def fmt_date(value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%b %d, %Y")
        except (TypeError, ValueError):
            return value

    return app
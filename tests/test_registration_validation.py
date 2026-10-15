import unittest

from app.routes.auth import validate_registration

from unittest.mock import patch, MagicMock


class TestRegistrationValidation(unittest.TestCase):

    # Test to check if full name is missing
    def test_missing_full_name(self):
        errors = validate_registration(
            full_name="",
            username="",
            email="",
            password=""
        )

        self.assertEqual(
            errors["full_name"],
            "Full name is required."
        )


    # Test to check if password is missing
    def test_missing_password(self):
        errors = validate_registration(
            full_name="John Smith",
            username="",
            email="",
            password=""
        )

        self.assertEqual(
            errors["password"],
            "Password is required."
        )


    # Test to check if username is already taken
    @patch("app.routes.auth.get_db")
    def test_duplicate_username(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_db.execute.return_value.fetchone.side_effect = [
            (1,),
            None
        ]

        errors = validate_registration(
            full_name="John Smith",
            username="existinguser",
            email="john@example.com",
            password="Password123!"
        )

        self.assertEqual(
            errors["username"],
            "Username is already taken."
        )


    # Test to check if email is already registered
    @patch("app.routes.auth.get_db")
    def test_duplicate_email(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_db.execute.return_value.fetchone.side_effect = [
            None,
            (1,)
        ]

        errors = validate_registration(
            full_name="John Smith",
            username="newuser",
            email="john@example.com",
            password="Password123!"
        )

        self.assertEqual(
            errors["email"],
            "Email is already registered."
        )


    # Test to check if email lookup is case insensitive
    @patch("app.routes.auth.get_db")
    def test_email_lookup_is_case_insensitive(self, mock_get_db):
        import sqlite3

        db = sqlite3.connect(":memory:")
        db.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, "
            "username TEXT, email TEXT)"
        )
        db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            ("existinguser", "john@example.com")
        )

        mock_get_db.return_value = db

        try:
            errors = validate_registration(
                full_name="John Smith",
                username="newuser",
                email="JOHN@EXAMPLE.COM",
                password="Password123!"
            )

            self.assertEqual(
                errors["email"],
                "Email is already registered."
            )
        finally:
            db.close()


    # Test to check if registration is valid
    @patch("app.routes.auth.get_db")
    def test_valid_registration(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_db.execute.return_value.fetchone.return_value = None

        errors = validate_registration(
            full_name="John Smith",
            username="newuser",
            email="john@example.com",
            password="Password123!"
        )

        self.assertEqual(errors, {})


    # Test to check if username is missing
    def test_missing_username(self):
        errors = validate_registration(
            full_name="John Smith",
            username="",
            email="",
            password="Password123!"
        )

        self.assertEqual(
            errors["username"],
            "Username is required."
        )


    # Test to check if email format is invalid
    def test_invalid_email_format(self):
        errors = validate_registration(
            full_name="John Smith",
            username="",
            email="johnexample.com",
            password="Password123!"
        )

        self.assertEqual(
            errors["email"],
            "Please enter a valid email address."
        )


    # Test to check if email is missing
    def test_missing_email(self):
        errors = validate_registration(
            full_name="John Smith",
            username="",
            email="",
            password="Password123!"
        )

        self.assertEqual(
            errors["email"],
            "Email is required."
        )
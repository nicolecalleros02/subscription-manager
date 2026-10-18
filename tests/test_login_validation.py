import unittest

from app.routes.auth import validate_login


class TestLoginValidation(unittest.TestCase):

    def test_valid_login_input(self):
        errors = validate_login("john123", "Password123!")
        self.assertEqual(errors, {})

    def test_missing_username(self):
        errors = validate_login("", "Password123!")
        self.assertIn("username", errors)

    def test_whitespace_username(self):
        errors = validate_login("   ", "Password123!")
        self.assertIn("username", errors)

    def test_missing_password(self):
        errors = validate_login("john123", "")
        self.assertIn("password", errors)

    def test_missing_both_fields(self):
        errors = validate_login("", "")
        self.assertIn("username", errors)
        self.assertIn("password", errors)


if __name__ == "__main__":
    unittest.main()
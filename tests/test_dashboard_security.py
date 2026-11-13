import unittest
import os
import tempfile

from app import create_app
from app.db import get_db

class TestDashboardSecurity(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the test database
        self.temp_dir = tempfile.TemporaryDirectory()

        # Set the path for the isolated test database
        self.db_path = os.path.join(
            self.temp_dir.name,
            "test_dashboard.db"
        )

        # Create the test app with the isolated database
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
            'DEMO_MODE': False
        })

        # Create a test client for making requests
        self.client = self.app.test_client()

    def tearDown(self):
        # Clean up the temporary directory and database
        self.temp_dir.cleanup()

    def test_unauthenticated_user_redirected(self):
        # Attempt to access dashboard without logging in
        response = self.client.get('/dashboard')

        # Verify Flask redirects the user
        self.assertEqual(response.status_code, 302)

        # Verify the redirect points to the login page
        self.assertIn('/login', response.location)

    def test_authenticated_user_can_access_dashboard(self):

        # Create a test user in the temporary database
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO users
                   (id, full_name, username, email, password_hash)
                   VALUES (1, 'Test User', 'testuser',
                           'testuser@example.com', 'test_hash')"""
            )
            db.commit()

        # Simulate a logged-in user
        with self.client.session_transaction() as session:
            session['user_id'] = 1

        # Attempt to access the dashboard
        response = self.client.get('/dashboard')

        # Verify the user can access the dashboard
        self.assertEqual(response.status_code, 200)
import unittest
import sqlite3
from unittest.mock import patch

from app.models.subscription import (
    create_subscription,
    get_subscriptions_by_user_id,
    get_subscription_by_id,
    update_subscription,
    delete_subscription
)


class TestSubscriptionSecurity(unittest.TestCase):

    def setUp(self):
        # Create an isolated in-memory database
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")

        # Create the tables using the project's schema
        with open("app/schema.sql", "r") as schema:
            self.db.executescript(schema.read())

        # Create two test users
        self.db.execute(
            """INSERT INTO users
               (id, full_name, username, email, password_hash)
               VALUES (1, 'User One', 'user1', 'user1@test.com', 'test')"""
        )

        self.db.execute(
            """INSERT INTO users
               (id, full_name, username, email, password_hash)
               VALUES (2, 'User Two', 'user2', 'user2@test.com', 'test')"""
        )
        self.db.commit()

        # Redirect subscription model database calls to our test database
        self.db_patch = patch(
            "app.models.subscription.get_db",
            return_value=self.db
        )
        self.db_patch.start()

        # Create a subscription owned by User 1
        self.subscription_id = create_subscription(
            1, "Netflix", 10.99, "monthly",
            "Entertainment", "2026-11-15"
        )

    def tearDown(self):
        self.db_patch.stop()
        self.db.close()

    def test_owner_can_view_subscription(self):
        subscription = get_subscription_by_id(
            1, self.subscription_id
        )
        self.assertIsNotNone(subscription)

    def test_other_user_cannot_view_subscription(self):
        subscription = get_subscription_by_id(
            2, self.subscription_id
        )
        self.assertIsNone(subscription)

    def test_other_user_cannot_list_subscription(self):
        subscriptions = get_subscriptions_by_user_id(2)
        self.assertEqual(subscriptions, [])

    def test_other_user_cannot_update_subscription(self):
        result = update_subscription(
            2, self.subscription_id, "Changed Name",
            20.00, "monthly", "Entertainment", "2026-11-15"
        )
        self.assertFalse(result)

        original = get_subscription_by_id(1, self.subscription_id)
        self.assertEqual(original["name"], "Netflix")

    def test_other_user_cannot_delete_subscription(self):
        result = delete_subscription(2, self.subscription_id)
        self.assertFalse(result)

        original = get_subscription_by_id(1, self.subscription_id)
        self.assertIsNotNone(original)
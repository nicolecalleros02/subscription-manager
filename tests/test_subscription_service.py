import unittest
from subscription_validation import validate_subscription


class TestSubscriptionValidation(unittest.TestCase):

    def test_valid_subscription(self):
        subscription = {
            "name": "Netflix",
            "price": "10.99",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(errors, {})

    def test_negative_price(self):
        subscription = {
            "name": "Netflix",
            "price": "-10.99",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["price"],
            "Price cannot be negative."
        )

    def test_missing_subscription_name(self):
        subscription = {
            "name": "",
            "price": "10.99",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["name"],
            "Subscription name is required."
        )

    def test_invalid_billing_cycle(self):
        subscription = {
            "name": "Netflix",
            "price": "10.99",
            "billing_cycle": "daily",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["billing_cycle"],
            "Please select a valid billing cycle."
        )

    def test_invalid_billing_date(self):
        subscription = {
            "name": "Netflix",
            "price": "10.99",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-02-30"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["next_billing_date"],
            "Please enter a valid date in YYYY-MM-DD format."
        )

    def test_invalid_cancellation_url(self):
        subscription = {
            "name": "Netflix",
            "price": "10.99",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15",
            "cancellation_url": "not-a-url"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["cancellation_url"],
            "Please enter a valid cancellation URL."
        )

    def test_missing_category(self):
        subscription = {
            "name": "Netflix",
            "price": "10.99",
            "billing_cycle": "monthly",
            "category": "",
            "next_billing_date": "2026-11-15"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["category"],
            "Subscription category is required."
        )

    def test_nonnumeric_price(self):
        subscription = {
            "name": "Netflix",
            "price": "abc",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15"
        }

        errors = validate_subscription(subscription)

        self.assertEqual(
            errors["price"],
            "Please enter a valid price."
        )

    def test_nonfinite_prices(self):
        subscription = {
            "name": "Netflix",
            "price": "10.99",
            "billing_cycle": "monthly",
            "category": "Entertainment",
            "next_billing_date": "2026-11-15"
        }

        for price in ["nan", "inf", "-inf"]:
            with self.subTest(price=price):
                subscription["price"] = price

                errors = validate_subscription(subscription)

                self.assertEqual(
                    errors["price"],
                    "Please enter a valid price."
                )
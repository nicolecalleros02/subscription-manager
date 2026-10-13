import math
from datetime import datetime
from urllib.parse import urlsplit

def validate_subscription(data):
    errors = {}

    name = data.get("name", "").strip()

    if not name:
        errors["name"] = "Subscription name is required."

    price = data.get("price")

    try:
        price = float(price)

        if not math.isfinite(price):
            errors["price"] = "Please enter a valid price."
        elif price < 0:
            errors["price"] = "Price cannot be negative."

    except (TypeError, ValueError):
        errors["price"] = "Please enter a valid price."

    billing_cycle = data.get("billing_cycle", "").strip().lower()

    valid_cycles = ["weekly", "monthly", "quarterly", "yearly"]

    if not billing_cycle:
        errors["billing_cycle"] = "Billing cycle is required."
    elif billing_cycle not in valid_cycles:
        errors["billing_cycle"] = "Please select a valid billing cycle."

    category = data.get("category", "").strip()

    if not category:
        errors["category"] = "Subscription category is required."

    next_billing_date = data.get("next_billing_date", "").strip()

    if not next_billing_date:
        errors["next_billing_date"] = "Next billing date is required."
    else:
        try:
            datetime.strptime(next_billing_date, "%Y-%m-%d")
        except ValueError:
            errors["next_billing_date"] = "Please enter a valid date in YYYY-MM-DD format."

    cancellation_url = data.get("cancellation_url", "").strip()

    if cancellation_url:
        try:
            parsed_url = urlsplit(cancellation_url)

            if (
                parsed_url.scheme not in ("http", "https")
                or not parsed_url.hostname
                or any(char.isspace() for char in cancellation_url)
            ):
                errors["cancellation_url"] = "Please enter a valid cancellation URL."

        except ValueError:
            errors["cancellation_url"] = "Please enter a valid cancellation URL."

    return errors

if __name__ == "__main__":
    subscription = {
        "name": "Netflix",
        "price": "10.99",
        "billing_cycle": "monthly",
        "category": "Entertainment",
        "next_billing_date": "2026-11-15"
    }

    print(validate_subscription(subscription))

    print(validate_subscription({
        **subscription,
        "cancellation_url": "https://www.netflix.com"
    }))

    print(validate_subscription({
        **subscription,
        "cancellation_url": "not-a-url"
    }))
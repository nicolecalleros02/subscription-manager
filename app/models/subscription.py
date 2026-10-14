from app.db import get_db

# Add new subscription
def create_subscription(user_id, name, price, billing_cycle, category, next_billing_date, cancellation_url=None, remind_renewal=True):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO subscriptions (user_id, name, price, billing_cycle, category, next_billing_date, cancellation_url, remind_renewal) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, name, price, billing_cycle, category, next_billing_date, cancellation_url, int(remind_renewal))
    )
    db.commit()
    return cursor.lastrowid 


# Get all subscriptions by user id
def get_subscriptions_by_user_id(user_id):
    rows = get_db().execute(
        "SELECT * FROM subscriptions WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    return [dict(row) for row in rows]  # returns a list of subscriptions as dictionaries for the given user id


# Get one subscription by user id and subscription id
def get_subscription_by_id(user_id, subscription_id):
    row = get_db().execute(
        "SELECT * FROM subscriptions WHERE user_id = ? AND id = ?",
        (user_id, subscription_id)
    ).fetchone()
    return dict(row) if row else None   # returns the subscription as a dictionary if found, otherwise None


# Update subscription by user id and subscription id
def update_subscription(user_id, subscription_id, name, price, billing_cycle, category, next_billing_date, cancellation_url=None, remind_renewal=True):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE subscriptions SET name = ?, price = ?, billing_cycle = ?, category = ?, next_billing_date = ?, cancellation_url = ?, remind_renewal = ? WHERE user_id = ? AND id = ?",
        (name, price, billing_cycle, category, next_billing_date, cancellation_url, int(remind_renewal), user_id, subscription_id)
    )
    db.commit()
    return cursor.rowcount > 0  # returns true if row was changed


# Delete subscription by user id and subscription id
def delete_subscription(user_id, subscription_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM subscriptions WHERE user_id = ? AND id = ?",
        (user_id, subscription_id)
    )
    db.commit()
    return cursor.rowcount > 0  # returns true if row was deleted
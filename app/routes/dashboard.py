from flask import Blueprint, render_template, session, redirect, url_for
from app.models.subscription import get_subscriptions_by_user_id

# Initialize blueprint for the dashboard route
bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():

    # Get the logged-in user's ID from the session
    user_id = session.get("user_id")

    # Redirect to login if the user is not authenticated
    if user_id is None:
        return redirect(url_for("auth.login"))

    # Get subscriptions belonging to the logged-in user
    subscriptions = get_subscriptions_by_user_id(user_id)

    # Calculate total monthly due
    total_due = 0.0
    for sub in subscriptions:
        total_due += sub['price']

    # Get total count of active subscriptions
    subscription_count = len(subscriptions)

    # Pass data to template
    return render_template(
        'dashboard.html',
        subscriptions=subscriptions,
        total_due=total_due,
        subscription_count=subscription_count
    )
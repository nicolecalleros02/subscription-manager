from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash
)

from app.models.subscription import (
    create_subscription,
    update_subscription,
    delete_subscription,
    get_subscription_by_id
)

bp = Blueprint('subscriptions', __name__)
#add, update, delete functions


# Read in user values then pass to "create_subscription()" to finish
def readCreateSubscription(user_id):
    name = request.form.get("name")
    price = request.form.get("price")
    billing_cycle = request.form.get("cycle")
    category = request.form.get("category")
    next_billing_date = request.form.get("billDate")
    cancellation_url = request.form.get("urlLink")
    remind_renewal = request.form.get("remind")

    validateCreation_Update(name, price, billing_cycle, category, next_billing_date, cancellation_url, remind_renewal)
    create_subscription(user_id, name, price, billing_cycle, category, next_billing_date, cancellation_url, remind_renewal)
    # Go back to dashboard
    return redirect(url_for())

# Read in user values then pass to "update_subscription()" to finish
def readUpdateSubscription(user_id):
    name = request.form.get("name")
    price = request.form.get("price")
    billing_cycle = request.form.get("cycle")
    category = request.form.get("category")
    next_billing_date = request.form.get("billDate")
    cancellation_url = request.form.get("urlLink")
    remind_renewal = request.form.get("remind")
    
    validateCreation_Update(name, price, billing_cycle, category, next_billing_date, cancellation_url, remind_renewal)
    update_subscription(user_id, name, price, billing_cycle, category, next_billing_date, cancellation_url, remind_renewal)
    # Go back to dashboard
    return redirect(url_for())

# Read in user values then pass to "delete_subscription()" to finish
def readDeleteSunscription(user_id):
    name = request.form.get("name")
    # Use the subscription name to get the id to pass through "delete_subscription()"
    delete_subscription(user_id, subscription_id)
    # Go back to dashboard
    return redirect(url_for())

# Validates that there's info in each field & that it's correct
def validateCreation_Update(name, price, billing_cycle, category, next_billing_date, cancellation_url, remind_renewal):

    # Go back to whatever function it came from
    return 
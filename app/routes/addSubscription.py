from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from app.models.subscription import (
    create_subscription,
    get_subscription_by_id,
    get_subscriptions_by_user_id
)

bp = Blueprint('addSubscription', __name__)

@bp.route('/addSubscription')
def tempAddSubscription():

    # Get the logged-in user's ID from the session
    user_id = session.get("user_id")

    # Redirect to login if the user is not authenticated
    if user_id is None:
        return redirect(url_for("auth.login"))

    return render_template('addSubscription.html')
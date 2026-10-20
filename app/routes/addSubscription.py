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
    get_subscription_by_id,
    get_subscriptions_by_user_id
)

bp = Blueprint('addSubscription', __name__)
@bp.route('/addSubscription')
def tempAddSubscription():
    user_id = 1 #temp
    return render_template('addSubscription.html')
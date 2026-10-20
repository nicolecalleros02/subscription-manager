from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash
)

from app.models.subscription import (
    update_subscription,
    get_subscription_by_id,
    get_subscriptions_by_user_id
)

bp = Blueprint('updateSubscription', __name__)
@bp.route('/updateSubscription')
def tempUpdateSubscription():
    user_id = 1 #temp
    return render_template('updateSubscription.html')
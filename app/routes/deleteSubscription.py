from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash
)

from app.models.subscription import (
    delete_subscription,
    get_subscription_by_id,
    get_subscriptions_by_user_id
)

bp = Blueprint('deleteSubscription', __name__)
@bp.route('/deleteSubscription')
def tempDeleteSubscription():
    user_id = 1 #temp
    return render_template('deleteSubscription.html')
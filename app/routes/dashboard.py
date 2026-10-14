from flask import Blueprint, render_template
from app.models.subscription import get_subscriptions_by_user_id

# Initialize blueprint for the dashboard route
bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():
    user_id = 1     # temp
    
    # Get list of subscriptions from db 
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
        total_due = total_due, 
        subscription_count=subscription_count
    )
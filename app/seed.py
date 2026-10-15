#demo data

from app import create_app
from app.models.user import create_user
from app.models.subscription import create_subscription

app = create_app()
with app.app_context():
    user_id = create_user("Demo User", "demo", "demo@example.com", "fake-hash")
    create_subscription(user_id, "Netflix Premium", 15.49, "Monthly", "Entertainment", "2026-10-18")
    create_subscription(user_id, "Spotify", 10.99, "Monthly", "Entertainment", "2026-10-22")
    create_subscription(user_id, "Adobe Creative Cloud", 54.99, "Monthly", "Software", "2026-11-05")
    print("Demo data added. User id:", user_id)
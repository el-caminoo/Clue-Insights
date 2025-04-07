from app import create_app
from config.database import db
from models import Plan, Currency
from datetime import datetime, timezone

app = create_app()

def seed_db():
  with app.app_context():
      # Create one shared plan
      plan = Plan(billing_interval=30, created_at=datetime.now(timezone.utc))
      db.session.add(plan)
      db.session.commit()

      # create currency to be used
      currency = Currency(
          code="USD", name="United States Dollars", created_at=datetime.now(timezone.utc)
      )
      db.session.add(currency)
      db.session.commit()

      print(f"✅ Added plan and currency to the database")

if __name__ == "__main__":
    seed_db()

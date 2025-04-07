from datetime import datetime, timezone
from models import Product, ProductPricing
from config.database import db

class ProductRepository:
    @staticmethod
    def create_new_subscription(data: dict, currency="USD", plan_id=1, created_at=datetime.now(timezone.utc)):
        """Insert a new product(subscription plan) into the database"""
        product = Product(
            name=data["name"],
            description=data["description"],
            price=[
                ProductPricing(
                    price=data["price"],
                    currency=currency,
                    from_date=data["from_date"],
                    to_date=data["to_date"],
                    created_at=created_at
                )
            ],
            plan_id=plan_id,
            created_at=created_at
        )

        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_all_subscription_plans():
        """Retrieves all available subscription plans from the database."""
        return db.session.query(Product).all()
    
    @staticmethod
    def get_subscription_plan_by_name(name):
        return db.session.query(Product).filter_by(name=name).first()
from datetime import datetime, timezone
from models import Customer
from config.database import db


class CustomerRepository:
    @staticmethod
    def create_customer(email, first_name, last_name, phone, country, password_hash, currency="USD"):
        """Insert a new customer into the database"""
        customer = Customer(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            country=country,
            password_hash=password_hash,
            currency_code=currency,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def get_customer_by_email(email):
        """Fetch a customer by email."""
        return db.session.query(Customer).filter_by(email=email).first()

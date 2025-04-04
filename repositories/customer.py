from config.database import db
from sqlalchemy import text


class CustomerRepository:
    @staticmethod
    def create_customer(email, first_name, last_name, phone, country, password_hash):
        """Insert a new customer into the database"""
        sql = text(
            "INSERT INTO customers (email, first_name, last_name, phone, country, password_hash) VALUES (:email, :first_name, " \
            ":last_name, :phone, :country, :password_hash)"
        )
        db.session.execute(
            sql, {"email": email, "first_name": first_name, "last_name": last_name, "phone": phone, 
                  "country": country, "password_hash": password_hash}
        )
        db.session.commit()

    @staticmethod
    def get_customer_by_email(email):
        """Fetch a customer by email."""
        sql = text("SELECT * FROM customers WHERE email = :email")
        return db.session.execute(sql, {"email": email}).fetchone()

    # @staticmethod
    # def delete_user(username):
    #     """Delete a user by username using raw SQL."""
    #     sql = "DELETE FROM users WHERE username = :username"
    #     db.session.execute(sql, {"username": username})
    #     db.session.commit()

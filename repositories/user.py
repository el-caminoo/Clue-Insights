from config.database import db
from sqlalchemy import text

class UserRepository:
    @staticmethod
    def create_user(email, password_hash, role):
        """Insert a new user into the database"""
        sql = text("INSERT INTO users (email, password_hash, role) VALUES (:email, :password_hash, :role)")
        db.session.execute(
            sql, {"email": email, "password_hash": password_hash, "role": role}
        )
        db.session.commit()

    @staticmethod
    def get_user_by_email(email):
        """Fetch a user by email."""
        sql = text("SELECT * FROM users WHERE email = :email")
        return db.session.execute(sql, {"email": email}).fetchone()

    # @staticmethod
    # def delete_user(username):
    #     """Delete a user by username using raw SQL."""
    #     sql = "DELETE FROM users WHERE username = :username"
    #     db.session.execute(sql, {"username": username})
    #     db.session.commit()

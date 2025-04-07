from config.database import db
from datetime import datetime, timezone
from models import User

class UserRepository:

  @staticmethod
  def _get_utc_now():
    return datetime.now(timezone.utc)

  @staticmethod
  def create_user(email, password_hash, role):
    """Insert a new user into the database"""
    user = User(
        email=email,
        password_hash=password_hash,
        role=role,
        created_at=UserRepository._get_utc_now()
    )
    db.session.add(user)
    db.session.commit()
    return user

  @staticmethod
  def get_user_by_email(email):
    """Fetch a user by email."""
    return db.session.query(User).filter_by(email=email).first()


from typing import Tuple, Dict, Any
from flask_jwt_extended import create_access_token
from repositories import UserRepository
from schemas import UserSchema
from .password import PasswordService
from utils import format_response
from datetime import timedelta

class UserService:

  @staticmethod
  def register_user(email: str, password: str, role: str) -> Tuple[Dict[str, Any], int]:
    """Register a new user if they don't already exist."""
    if UserRepository.get_user_by_email(email):
      return format_response("Email already exists", success=False, status=400)

    hashed_password = PasswordService.hash_password(password)
    user = UserRepository.create_user(email, hashed_password, role)
    serialized_user = UserSchema().dump(user)

    return format_response(
        "User registered successfully", serialized_user, status=201
    )

  @staticmethod
  def authenticate_user(email: str, password: str) -> Tuple[Dict[str, Any], int]:
    """Authenticate a user and return a JWT token."""
    user = UserRepository.get_user_by_email(email)

    if user and PasswordService.verify_password(password, user.password_hash):
      access_token = create_access_token(
        identity=str(user.role), fresh=True, expires_delta=timedelta(days=1)
      )

      return format_response("Authentication successful", {"access_token": access_token})

    return format_response(
        "Invalid credentials", success=False, status=400
    )

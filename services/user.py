from flask_jwt_extended import create_access_token
from repositories import UserRepository
from .password import PasswordService

class UserService:

  @staticmethod
  def register_user(email, password, role):
    """Register a new user if they don't already exist."""
    existing_user = UserRepository.get_user_by_email(email)
    if existing_user:
      return {"message": "Email already exists", "success": False}, 400

    hashed_password = PasswordService.hash_password(password)
    UserRepository.create_user(email, hashed_password, role)
    return {"message": "User registered successfully", "success": True}, 201

  @staticmethod
  def authenticate_user(email, password):
    """Authenticate a user by verifying the password."""
    user = UserRepository.get_user_by_email(email)
    if user and PasswordService.verify_password(password, user.password_hash):
      # Create JWT token
      access_token = create_access_token(identity={"user_id": user.id, "role": user.role}, fresh=True)
      return {
              "message": "Authentication successful",
              "access_token": access_token,
              "success": True,
            }, 200
    
    return {"message": "Invalid credentials", "success": False}, 400

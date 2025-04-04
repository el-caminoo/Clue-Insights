from flask_jwt_extended import create_access_token
from repositories import CustomerRepository
from .password import PasswordService

class CustomerService:

  @staticmethod
  def register_customer(data):
    """Registers a new customer if they don't already exist."""
    email = data.get("email")
    existing_customer = CustomerRepository.get_customer_by_email(email)
    if existing_customer:
      return {"message": "Email already exists", "success": False}, 400
    
    password = data.get("password")
    hashed_password = PasswordService.hash_password(password)

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone = data.get("phone")
    country = data.get("country")

    CustomerRepository.create_customer(email, first_name, last_name, phone, country, hashed_password)
    return {"message": "Customer registered successfully", "success": True}, 201

  @staticmethod
  def authenticate_customer(email, password):
    """Authenticate a customer by verifying the password."""
    customer = CustomerRepository.get_customer_by_email(email)
    if customer and PasswordService.verify_password(password, customer.password_hash):
      # Create JWT token
      access_token = create_access_token(identity={"id": customer.id}, fresh=True)
      return {
                "message": "Authentication successful",
                "access_token": access_token,
                "success": True,
            }, 200

    return {"message": "Invalid credentials", "success": False}, 400

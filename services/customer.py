from flask_jwt_extended import create_access_token
from utils import format_response
from datetime import timedelta
from repositories import CustomerRepository
from schemas import CustomerSchema
from typing import Tuple, Dict, Any
from .password import PasswordService

class CustomerService:

  @staticmethod
  def register_customer(data: dict) -> Tuple[Dict[str, Any], int]:
    """Registers a new customer if they don't already exist."""
    if CustomerRepository.get_customer_by_email(data["email"]):
      return format_response("Email already exists", success=False, status=400)

    hashed_password = PasswordService.hash_password(data["password"])

    customer = CustomerRepository.create_customer(
    email=data.get("email"),
    first_name=data.get("first_name"),
    last_name=data.get("last_name"),
    phone=data.get("phone"),
    country=data.get("country"),
    password_hash=hashed_password,
      )

    serialized = CustomerSchema().dump(customer)
    return format_response("Customer registered successfully", serialized, status=201)

  @staticmethod
  def authenticate_customer(email: str, password: str) -> Tuple[Dict[str, Any], int]:
    """Authenticate a customer by verifying the password."""
    customer = CustomerRepository.get_customer_by_email(email)

    if customer and PasswordService.verify_password(password, customer.password_hash):
        access_token = create_access_token(
          identity=str(customer.id), fresh=True, expires_delta=timedelta(days=1)
      )
        return format_response(
            "Authentication successful",
            {"access_token": access_token},
        )

    return format_response(
    "Invalid credentials", success=False, status=400
  )

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Customer

class CreateCustomerSchema(Schema):
    """Schema for creating a new customer"""

    email = fields.String(required=True, description="Email of the customer")
    first_name = fields.String(required=True, description="First name of the customer")
    last_name = fields.String(required=True, description="Last name of the customer")
    phone = fields.String(required=True, description="Phone number of the customer")
    country = fields.String(required=True, description="Country of residence of the customer")
    password = fields.String(required=True, load_only=True, description="Password for authentication")


class AuthenticateCustomerSchema(Schema):
    """Schema for customer login"""

    email = fields.String(required=True, description="email of the customer")
    password = fields.String(required=True, load_only=True, description="Password for authentication")


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        exclude = ("id", "password_hash", "currency_id", "created_at", "deleted_at")

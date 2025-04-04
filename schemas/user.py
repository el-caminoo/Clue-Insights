from marshmallow import Schema, fields


class CreateUserSchema(Schema):
    """Schema for creating a new user"""

    email = fields.String(required=True, description="Email of the user")
    password = fields.String(required=True, load_only=True, description="Password for authentication")
    role = fields.String(required=True, description="Authorization level of the user")


class AuthenticateUserSchema(Schema):
    """Schema for user login"""

    email = fields.String(required=True, description="Email of the user")
    password = fields.String(required=True, load_only=True, description="Password for authentication")

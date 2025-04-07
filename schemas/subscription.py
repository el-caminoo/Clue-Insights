from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Subscription, Customer
from .product import ProductSubscriptionSchema

class SubscriptionQuerySchema(Schema):
    status = fields.String(required=False)
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)

class PurchaseSubscriptionSchema(Schema):
    """Schema for purchasing a new subscription"""

    product_id = fields.Int(required=True, description="ID of the product to subscribe to.")
    price = fields.Float(required=True, description="Price of the product")
    validity_period = fields.Int(required=True, description="Subscription validity period")

class UpgradeSubscriptionSchema(Schema):
    """Schema for upgrading to a new subscription"""

    product_id = fields.Int(required=True, description="ID of the product to upgrade to.")
    price = fields.Float(required=True, description="Price of the product")
    validity_period = fields.Int(required=True, description="Subscription validity period")

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        exclude = ("id", "password_hash", "created_at", "deleted_at")


class SubscriptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription
        load_instance = True
        exclude = ("customer_id", "created_at", "deleted_at")
    
    customer = fields.Nested(CustomerSchema)
    product = fields.Nested(ProductSubscriptionSchema)
    downgraded_to_product = fields.Nested(ProductSubscriptionSchema)
    upgraded_to_product = fields.Nested(ProductSubscriptionSchema)

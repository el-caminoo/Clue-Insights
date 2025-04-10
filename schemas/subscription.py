from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Subscription
from .product import ProductSchema
from .customer import CustomerSchema

class SubscriptionQuerySchema(Schema):
    page = fields.Int(missing=1, validate=validate.Range(min=1), description="Page number")
    page_size = fields.Int(missing=10, validate=validate.Range(min=1, max=100), description="Number of items per page")
    
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

class SubscriptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription
        load_instance = True
        exclude = ("customer_id", "created_at", "deleted_at")
    
    customer = fields.Nested(CustomerSchema)
    product = fields.Nested(ProductSchema)
    downgraded_to_product = fields.Nested(ProductSchema)
    upgraded_to_product = fields.Nested(ProductSchema)

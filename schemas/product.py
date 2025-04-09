from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
from models import Product
from schemas.plan import PlanSchema
from schemas.pricing import ProductPricingSchema


class CreateProductSchema(Schema):
    """Schema for creating a new product(Subscription plan)"""

    name = fields.String(required=True, description="Name of the product(subscription)")
    description = fields.String(required=True, description="Description of the product(subscription)")
    amount = fields.Integer(required=True, description="Price of the subscription")
    from_date = fields.Date(required=True, description="The date the price starts applying")
    to_date = fields.Date(required=True, description="The date the price stops applying")

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        exclude = ("plan_id", "created_at", "deleted_at")

    price = fields.List(fields.Nested(ProductPricingSchema))
    plan = fields.Nested(PlanSchema)


class ProductSubscriptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        exclude = ("plan_id", "created_at", "deleted_at")

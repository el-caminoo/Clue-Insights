from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import ProductPricing


class ProductPricingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductPricing
        load_instance = True
        include_fk = True
        exclude = ("id", "created_at", "deleted_at", "product_id")


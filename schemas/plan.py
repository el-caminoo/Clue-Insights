from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Plan


class PlanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plan
        load_instance = True
        include_fk = True
        exclude = ("id", "created_at", "deleted_at")


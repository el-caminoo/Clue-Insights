from typing import Tuple, Dict, Any
from flask.views import MethodView
from flask_smorest import Blueprint
from utils import create_api_response
from decorators import admin_required
from schemas import ResponseSchema, CreateProductSchema
from services import ProductService

product_routes = Blueprint(
    "Product",
    "product",
    url_prefix="/product",
    description="Product related operations",
)

@product_routes.route("/create")
class CreateSubscriptionPlan(MethodView):
    @product_routes.arguments(CreateProductSchema)
    @product_routes.response(201, ResponseSchema)
    @admin_required
    def post(self, data: dict) -> Tuple[Dict[str, Any], int]:
      """Creates a new subscription plan."""
      response_data, status = ProductService.create_new_subscription(data)

      return (
        create_api_response(
          response_data["message"],
          response_data.get("data") if response_data["success"] else None,
          status,
          (None if response_data["success"] else "Failed to create subscription plan")), status
        )

@product_routes.route("/list")
class ListSubscriptionPlans(MethodView):
    @product_routes.response(200, ResponseSchema)
    def get(self) -> Tuple[Dict[str, Any], int]:
        """Fetches all available subscription plans."""
        response_data, status = ProductService.get_all_subscription_plans()

        return (
            create_api_response(
                response_data["message"],
                response_data.get("data") if response_data["success"] else None,
                status,
                (
                    None
                    if response_data["success"]
                    else "Unable to fetch subscription plans"
                ),
            ),
            status,
        )

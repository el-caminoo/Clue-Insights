from schemas import ProductSchema
from utils import format_response
from repositories import ProductRepository
from typing import Tuple, Dict, Any


class ProductService:

  @staticmethod
  def create_new_subscription(data: dict) -> Tuple[Dict[str, Any], int]:
    """Creates a new subscription plan with a unique name."""
    if ProductRepository.get_subscription_plan_by_name(data["name"]):
      return format_response(
        "Subscription plan with this name already exists",
        success=False,
        status=400,
      )

    product = ProductRepository.create_new_subscription(data)
    serialized = ProductSchema().dump(product)

    return format_response(
      "Subscription plan successfully created", serialized, status=201
    )

  @staticmethod
  def get_all_subscription_plans() -> Tuple[Dict[str, Any], int]:
    """Retrieves all available subscription plans."""
    subscriptions = ProductRepository.get_all_subscription_plans()
    serialized = ProductSchema(many=True).dump(subscriptions)

    return format_response(
      "Successfully retrieved subscriptions", serialized
    )

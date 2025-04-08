from typing import Tuple, Dict, Any
from schemas import SubscriptionSchema
from utils import format_response
from repositories import SubscriptionRepository

class SubscriptionService:

  @staticmethod
  def purchase_subscription(customer_id: int, data: dict) -> Tuple[Dict[str, Any], int]:
      """Purchases a new subscription for a customer."""
      subscription = SubscriptionRepository.purchase_subscription(customer_id, data)
      serialized = SubscriptionSchema().dump(subscription)
      return format_response(
          "Subscription purchased successfully.", serialized
      )

  @staticmethod
  def upgrade_subscription(customer_id: int, data: dict) -> Tuple[Dict[str, Any], int]:
      """Upgrades a user to a new subscription."""
      subscription = SubscriptionRepository.upgrade_subscription(customer_id, data)
      serialized = SubscriptionSchema().dump(subscription)
      return format_response(
          "Successfully upgraded subscription", serialized
      )

  @staticmethod
  def cancel_subscription(customer_id: int) -> Tuple[Dict[str, Any], int]:
      """Cancels a user's active subscription."""
      subscription = SubscriptionRepository.cancel_subscription(customer_id)
      serialized = SubscriptionSchema().dump(subscription)
      return format_response(
          "Successfully cancelled subscription", serialized
      )

  @staticmethod
  def get_active_subscriptions(limit, offset) -> Tuple[Dict[str, Any], int]:
      """Retrieves all active subscriptions."""
      subscriptions = SubscriptionRepository.get_active_subscriptions(limit, offset)
      serialized = SubscriptionSchema(many=True).dump(subscriptions)
      return format_response(
          "Successfully retrieved active subscriptions", serialized
      )

  @staticmethod
  def list_subscriptions(limit, offset) -> Tuple[Dict[str, Any], int]:
      """Returns all subscriptions."""
      subscriptions = SubscriptionRepository.list_subscriptions(limit, offset)
      serialized = SubscriptionSchema(many=True).dump(subscriptions)
      return format_response(
          "Successfully retrieved subscriptions", serialized
      )

  @staticmethod
  def retrieve_customer_subscription_history(customer_id: int, limit, offset) -> Tuple[Dict[str, Any], int]:
      """Retrieves a customer's subscription history (sorted)."""
      subscriptions = SubscriptionRepository.retrieve_customer_subscription_history(
          customer_id, limit, offset
      )
      serialized = SubscriptionSchema(many=True).dump(subscriptions)
      return format_response(
          "Successfully retrieved subscriptions history", serialized
      )

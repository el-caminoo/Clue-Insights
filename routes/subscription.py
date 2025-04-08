from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from utils import create_api_response, paginate
from schemas import ResponseSchema, UpgradeSubscriptionSchema, PurchaseSubscriptionSchema, SubscriptionQuerySchema
from services import SubscriptionService

subscription_routes = Blueprint(
    "Subscription",
    "subscription",
    url_prefix="/subscription",
    description="Subscription related operations",
)

@subscription_routes.route("/purchase")
class PurchaseSubscription(MethodView):
    @subscription_routes.arguments(PurchaseSubscriptionSchema)
    @subscription_routes.response(200, ResponseSchema)
    @jwt_required()
    def post(self, data: dict) -> dict:
        """Purchases a new subscription for a customer."""
        customer_id = get_jwt_identity()
        response_data, status = SubscriptionService.purchase_subscription(customer_id, data)

        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Purchase failed",
            ),
            status,
        )

@subscription_routes.route("/upgrade")
class UpgradeSubscription(MethodView):
    @subscription_routes.arguments(UpgradeSubscriptionSchema)
    @subscription_routes.response(200, ResponseSchema)
    @jwt_required()
    def post(self, data: dict) -> dict:
        """Upgrades a customer to a different subscription."""
        customer_id = get_jwt_identity()
        response_data, status = SubscriptionService.upgrade_subscription(customer_id, data)

        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Unsuccessful subscription upgrade",
            ),
            status,
        )

@subscription_routes.route("/cancel")
class CancelSubscription(MethodView):
    @subscription_routes.response(200, ResponseSchema)
    @jwt_required()
    def post(self) -> dict:
        """Cancels a user's active subscription."""
        customer_id = get_jwt_identity()
        response_data, status = SubscriptionService.cancel_subscription(customer_id)

        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Failed to cancel subscription",
            ),
            status,
        )

@subscription_routes.route("/active/all")
class RetrieveAllActiveSubscriptions(MethodView):
    @subscription_routes.arguments(SubscriptionQuerySchema, location="query")
    @subscription_routes.response(201, ResponseSchema)
    def get(self, query_args: dict) -> dict:
        """Returns a list of all active subscriptions."""

        page = query_args["page"]
        page_size = query_args["page_size"]

        limit, offset = paginate(page, page_size)

        response_data, status = SubscriptionService.get_active_subscriptions(limit, offset)

        return (create_api_response(
            response_data["message"],
            response_data["data"],
            status,
            None if response_data["success"] else "Unable to fetch active subscriptions",
        ), status
    )

@subscription_routes.route("/list")
class ListSubscriptions(MethodView):
    @subscription_routes.arguments(SubscriptionQuerySchema, location="query")
    @subscription_routes.response(200, ResponseSchema)
    def get(self, query_args: dict) -> dict:
        """Lists subscriptions."""

        page = query_args["page"]
        page_size = query_args["page_size"]

        limit, offset = paginate(page, page_size)

        response_data, status = SubscriptionService.list_subscriptions(limit, offset)

        return(
            create_api_response(
                response_data["message"], 
                response_data["data"], 
                status, 
                None if response_data["success"] else "Unable to fetch subscriptions"
            ), status
        )

@subscription_routes.route("/customer/history")
class RetrieveSubscriptionHistory(MethodView):
    @subscription_routes.arguments(SubscriptionQuerySchema, location="query")
    @subscription_routes.response(200, ResponseSchema)
    @jwt_required()
    def get(self, query_args: dict) -> dict:
        """Retrieves customer's subscription history."""

        customer_id = get_jwt_identity()

        page = query_args["page"]
        page_size = query_args["page_size"]

        limit, offset = paginate(page, page_size)

        response_data, status = SubscriptionService.retrieve_customer_subscription_history(customer_id, limit, offset)

        return(
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Unable to get subscription history"
            ), status
        )

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils import ApiResponse
from schemas import ResponseSchema, CreateCustomerSchema, AuthenticateCustomerSchema
from services import CustomerService

customer_routes = Blueprint(
    "Customer",
    "customer",
    url_prefix="/customer",
    description="Operation to create and authenticate customers to the platform",
)

@customer_routes.route("/create")
class CreateUser(MethodView):
    @customer_routes.arguments(CreateCustomerSchema)
    @customer_routes.response(201, ResponseSchema)
    def post(self, data):
        """Creates a new customer"""
        response_data, status = CustomerService.register_customer(data)
        response = ApiResponse(response_data["message"], None, status, None if response_data["success"] else "Registration failed")
        return response.to_dict(), status


@customer_routes.route("/login")
class AuthenticateUser(MethodView):
    @customer_routes.arguments(AuthenticateCustomerSchema)
    @customer_routes.response(200, ResponseSchema)
    def post(self, data):
        """Authenticates an existing customer to the platform"""
        response = ApiResponse("User created", None, 200, None)
        return response.to_dict(), 200

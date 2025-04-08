from flask.views import MethodView
from flask_smorest import Blueprint
from utils import create_api_response
from schemas import ResponseSchema, CreateCustomerSchema, AuthenticateCustomerSchema
from services import CustomerService

customer_routes = Blueprint(
    "Customer",
    "customer",
    url_prefix="/customer",
    description="Customer related operations",
)

@customer_routes.route("/create")
class CreateCustomer(MethodView):
    @customer_routes.arguments(CreateCustomerSchema)
    @customer_routes.response(201, ResponseSchema)
    def post(self, data: dict) -> dict:
        """Creates a new customer."""
        response_data, status = CustomerService.register_customer(data)

        # Create the response based on success/failure
        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Registration failed",
            ),
            status,
        )

@customer_routes.route("/login")
class AuthenticateCustomer(MethodView):
    @customer_routes.arguments(AuthenticateCustomerSchema)
    @customer_routes.response(200, ResponseSchema)
    def post(self, data: dict) -> dict:
        """Authenticates an existing customer to the platform."""
        email, password = data["email"], data["password"]

        response_data, status = CustomerService.authenticate_customer(
            email, password
        )

        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Login failed",
            ),
            status,
        )

from flask.views import MethodView
from flask_smorest import Blueprint
from utils import create_api_response
from schemas import ResponseSchema, CreateUserSchema, AuthenticateUserSchema
from services import UserService

user_routes = Blueprint(
    "User",
    "user",
    url_prefix="/user",
    description="User related operations",
)

@user_routes.route("/create")
class CreateUser(MethodView):
    @user_routes.arguments(CreateUserSchema)
    @user_routes.response(201, ResponseSchema)
    def post(self, data: dict) -> dict:
        """Creates a new user."""
        email, password, role = data["email"], data["password"], data["role"]

        response_data, status = UserService.register_user(email, password, role)

        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Registration failed",
            ),
            status,
        )

@user_routes.route("/login")
class AuthenticateUser(MethodView):
    @user_routes.arguments(AuthenticateUserSchema)
    @user_routes.response(200, ResponseSchema)
    def post(self, data: dict) -> dict:
        """Authenticates a user."""
        email, password = data["email"], data["password"]

        response_data, status = UserService.authenticate_user(email, password)

        return (
            create_api_response(
                response_data["message"],
                response_data["data"],
                status,
                None if response_data["success"] else "Login failed",
            ),
            status,
        )

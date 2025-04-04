from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils import ApiResponse
from schemas import ResponseSchema, CreateUserSchema, AuthenticateUserSchema
from services import UserService

user_routes = Blueprint("User", "user", url_prefix="/user", description="Operation to create and authenticate users")

@user_routes.route("/create")
class CreateUser(MethodView):
    @user_routes.arguments(CreateUserSchema)
    @user_routes.response(201, ResponseSchema)
    def post(self, data):
        """Creates a new User"""
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        response_data, status = UserService.register_user(email, password, role)
        response = ApiResponse(response_data["message"], None, status, None if response_data["success"] else "Registration failed")
        return response.to_dict(), status


@user_routes.route("/login")
class AuthenticateUser(MethodView):
    @user_routes.arguments(AuthenticateUserSchema)
    @user_routes.response(200, ResponseSchema)
    def post(self, data):
        """Authenticates an existing user to the platform"""

        email = data.get("email")
        password = data.get("password")

        response_data, status = UserService.authenticate_user(email, password)
        response = ApiResponse(
            response_data["message"],
            {"access_token": response_data["access_token"]} if response_data["success"] else None,
            status,
            None if response_data["success"] else "Login failed",
        )
        return response.to_dict(), status

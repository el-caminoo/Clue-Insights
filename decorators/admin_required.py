from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def admin_required(fn):
  """
  Decorator to restrict access to the route to only admin users.
  """
  @wraps(fn)
  @jwt_required()
  def wrapper(*args, **kwargs):
      # Get the current user's identity (user role)
      user = get_jwt_identity()
      
      if not user or user != "admin":
        return jsonify({"message": "Admin access required"}), 401
      return fn(*args, **kwargs)

  return wrapper

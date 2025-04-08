from typing import Generic, TypeVar, Optional, Tuple, Dict, Any

T = TypeVar("T")

class ApiResponse(Generic[T]):
  def __init__(self, message: str, data: Optional[T] = None, status: int = 200, error: Optional[str] = None):
      self.message = message
      self.data = data
      self.status = status
      self.error = error

  def __repr__(self):
      return f"ApiResponse(message={self.message!r}, data={self.data!r}, status={self.status}, error={self.error!r})"

  def to_dict(self):
      return {"message": self.message, "data": self.data, "status": self.status, "error": self.error}


def create_api_response(message: str, data: dict = None, status_code: int = 200, error: str = None) -> dict:
    """Helper function to create a standardized API response."""
    return ApiResponse(message, data, status_code, error).to_dict()

def format_response(message: str, data: Any = None, success: bool = True, status: int = 200) -> Tuple[Dict[str, Any], int]:
    return {
        "message": message,
        "data": data if success else None,
        "success": success,
    }, status

def paginate(page: int = 1, page_size: int = 10):
    """
    Calculates offset and limit for SQL pagination.
    """
    page = max(page, 1)
    offset = (page - 1) * page_size
    return page_size, offset
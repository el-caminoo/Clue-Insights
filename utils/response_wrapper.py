from typing import Generic, TypeVar, Optional

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

from marshmallow import Schema, fields

class ResponseSchema(Schema):
  """Standard response schema"""
  message = fields.String(description="Response message")
  data = fields.Raw(allow_none=True, description="Response data (None, Dict, or List of Dict)")
  status = fields.Integer(description="HTTP status code")
  error = fields.String(description="Error message if any", allow_none=True)

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "Clue Insights API"
    API_VERSION = "v0.0.1"
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_DESCRIPTION = "Love is trash"
    OPENAPI_URL_PREFIX = "/doc"
    OPENAPI_SWAGGER_UI_PATH = "/"
    # OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_SWAGGER_UI_URL = "/static/swagger-ui/dist/"
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    API_SPEC_OPTIONS = {
    "x-speakeasy-retries": {
      "strategy": "backoff",
      "backoff": {
        "initialInterval": 500,
        "maxInterval": 60000,
        "maxElapsedTime": 3600000,
        "exponent": 1.5,
      },
      "statusCodes": ["5XX"],
      "retryConnectionErrors": True,
  }
}

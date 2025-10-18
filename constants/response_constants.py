SERVER_STATUS_CODES = {
  "SUCCESS": {"code": 200, "message": "Request was successful"},
  "CREATED": {"code": 201, "message": "Resource created successfully"},
  "BAD_REQUEST": {"code": 400, "message": "Bad request"},
  "UNAUTHORIZED": {"code": 401, "message": "Unauthorized access"},
  "FORBIDDEN": {"code": 403, "message": "Forbidden"},
  "NOT_FOUND": {"code": 404, "message": "Resource not found"},
  "INTERNAL_SERVER_ERROR": {"code": 500, "message": "Internal server error"},
  "SERVICE_UNAVAILABLE": {"code": 503, "message": "Service unavailable"},
}


class StatusCode:
  def __init__(self, code, message):
    self.CODE = code
    self.MESSAGE = message


class ServerStatus:
  SUCCESS = StatusCode(200, "Request was successful")
  CREATED = StatusCode(201, "Resource created successfully")
  BAD_REQUEST = StatusCode(400, "Bad request")
  UNAUTHORIZED = StatusCode(401, "Unauthorized access")
  FORBIDDEN = StatusCode(403, "Forbidden")
  NOT_FOUND = StatusCode(404, "Resource not found")
  INTERNAL_SERVER_ERROR = StatusCode(500, "Internal server error")
  SERVICE_UNAVAILABLE = StatusCode(503, "Service unavailable")


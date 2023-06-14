# ======================= SHARED ERROR CODES TO be USED ON API =======================

# 10000 - 19999: Authentication
UNAUTHORIZED = 10000
INVALID_TOKEN = 10001
INVALID_CREDENTIALS = 10002
EXPIRED_TOKEN = 10003
INVALID_AUTHORIZATION_METHOD = 10004
FORBIDDEN = 10010

# 20000 - 29999: User
USER_NOT_FOUND = 20000
EMAIL_ALREADY_EXISTS = 20001
PHONE_ALREADY_EXISTS = 20002
PASSWORD_TOO_SHORT = 20101
PASSWORD_DOES_NOT_MATCH = 20102

# 30000 - 39999: Service
SERVICE_NOT_FOUND = 30000

# 40000 - 49999: Appointment

# 50000 - 59999: Organization
ORGANIZATION_NOT_FOUND = 50000
USER_ALREADY_HAS_ORGANIZATION = 50001

# 90000 - 99999: Internal server
INTERNAL_SERVER_ERROR = 90000
UNKNOWN_ERROR = 99999
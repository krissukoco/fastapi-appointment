# ======================= SHARED ERROR CODES TO be USED ON API =======================

# 10000 - 14999: Authentication
UNAUTHORIZED = 10000
INVALID_TOKEN = 10001
INVALID_CREDENTIALS = 10002
EXPIRED_TOKEN = 10003
INVALID_AUTHORIZATION_METHOD = 10004
FORBIDDEN = 10010

# 15000 - 19999: Common errors
INVALID_TIMEZONE = 15000

# 20000 - 29999: User
USER_NOT_FOUND = 20000
EMAIL_ALREADY_EXISTS = 20001
PHONE_ALREADY_EXISTS = 20002
PASSWORD_TOO_SHORT = 20101
PASSWORD_DOES_NOT_MATCH = 20102

# 30000 - 39999: Service
SERVICE_NOT_FOUND = 30000
SERVICE_START_TIME_CANNOT_BE_GREATER_THAN_END_TIME = 31001
SERVICE_APPOINTEES_MUST_BE_FILLED = 31002
SERVICE_APPOINTEES_MUST_BE_UNIQUE = 31003
SERVICE_APPOINTEES_MUST_BE_IN_ORGANIZATION = 31004
SERVICE_INVALID_GAP = 31005
SERVICE_INVALID_BREAK_TIME = 31006
SERVICE_NONUNIQUE_DAYS = 31007
SERVICE_NONUNIQUE_APPOINTEES = 31008
SERVICE_INVALID_TOTAL_DURATION = 31009
SERVICE_APPOINTEE_NOT_FOUND = 31010

# 40000 - 49999: Appointment

# 50000 - 59999: Organization
ORGANIZATION_NOT_FOUND = 50000
USER_ALREADY_HAS_ORGANIZATION = 50001
USER_HAS_NO_ORGANIZATION = 50002

# 80000 - 89999: Database

# 90000 - 99999: Internal server
INTERNAL_SERVER_ERROR = 90000
UNKNOWN_ERROR = 99999
from datetime import datetime

def current_timestamp() -> int:
    """
    Get current timestamp in milliseconds
    """
    return int(datetime.utcnow().timestamp() * 1000)
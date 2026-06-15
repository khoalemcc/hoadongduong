import os
from slowapi import Limiter
from slowapi.util import get_remote_address

is_testing = os.getenv("TESTING", "False").lower() in ("true", "1", "yes")

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not is_testing
)

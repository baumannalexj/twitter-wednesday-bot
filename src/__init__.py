import logging
import os
from datetime import datetime, timezone

from .date_helper import is_wednesday_for_tz

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"

logging.root.setLevel(LOG_LEVEL)

print("Main __init__ loaded")



if __name__ == '__main__':
    print(datetime.now(timezone.utcoffset(14)))
    print(logging.root)

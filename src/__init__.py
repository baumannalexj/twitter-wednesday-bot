import logging
import os
from datetime import datetime, timezone

from src.date_helper import is_wednesday

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"

logging.root.setLevel(LOG_LEVEL)



if __name__ == '__main__':
    print(datetime.now(timezone.utcoffset(14)))
    print(logging.root)

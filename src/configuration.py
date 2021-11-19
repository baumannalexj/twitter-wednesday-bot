import logging
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
logging.root.setLevel(LOG_LEVEL)

print(f"LOG_LEVEL:{LOG_LEVEL}")


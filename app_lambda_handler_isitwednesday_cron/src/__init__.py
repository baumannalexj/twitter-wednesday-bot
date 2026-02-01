import logging

from src import configuration

log_level = configuration.LOG_LEVEL
logging.root.setLevel(log_level)

print(f"isitwednesday_cron LOG_LEVEL:{log_level}")

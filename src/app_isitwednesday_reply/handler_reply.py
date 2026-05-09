import logging
import os
from datetime import datetime
from typing import Any

from app_config.config import config
from app_isitwednesday_reply import app_reply_module
from core.date_helper import get_time_min_ago


def lambda_handler(event, context):
    logging.info(f"{event=}")

    if _is_dry_run(event):
        logging.info("DRY_RUN — skipping Twitter call")
        return {"status": "DRY_RUN invoke ok"}

    start_time: datetime = get_time_min_ago(minutes_ago=config.reply_cron_interval_minutes)
    logging.info(f"Replying to wednesday tweets since {start_time.isoformat()}")
    app_reply_module.post_service.reply_to_recent_wednesday_tweets(start_time_iso=start_time)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {"status": "success", "message": "Scan for recent hashtag tweets complete."},
    }


def _is_dry_run(event) -> bool | None | Any:
    return str(os.environ.get("DRY_RUN")) == "true" or (isinstance(event, dict) and event.get("dry_run"))

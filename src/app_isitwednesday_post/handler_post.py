import logging
import os
from typing import Any

from app_isitwednesday_post import post_service


def lambda_handler(event, context):
    logging.info(f"{event=}")

    if _is_dry_run(event):
        logging.info("DRY_RUN — skipping Twitter call")
        return {"status": "dry_run_ok"}

    post_service.check_if_wednesday_and_post()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {"status": "success", "message": "Finished posting for today."},
    }


def _is_dry_run(event) -> bool | None | Any:
    return os.environ.get("DRY_RUN") == "true" or (isinstance(event, dict) and event.get("dry_run"))

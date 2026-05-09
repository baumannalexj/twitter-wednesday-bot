import logging
import os

from app_isitwednesday_post import app_post_module


def lambda_handler(event, context):
    logging.info(f"{event=}")

    if _is_dry_run(event):
        logging.info("DRY_RUN — skipping Twitter call")
        return {"status": "dry_run_ok"}

    app_post_module.post_service.check_if_wednesday_and_post()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {"status": "success", "message": "Finished posting for today."},
    }


def _is_dry_run(event) -> bool:
    return bool(
        os.environ.get("DRY_RUN") == "true"
        or (isinstance(event, dict) and event.get("dry_run"))
    )

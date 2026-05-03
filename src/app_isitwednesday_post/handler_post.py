import logging

from app_isitwednesday_post import app


def lambda_handler(event, context):
    logging.info(f"{event=}")
    app.wednesday_service.post_for_today()

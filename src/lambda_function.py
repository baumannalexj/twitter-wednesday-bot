import logging

from core import wednesday_service


def lambda_handler(event, context):
    logging.info(f"event:{event}")
    wednesday_service.post_for_today()

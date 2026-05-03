import logging
import os

from app_isitwednesday_reply.app_module import app_module
from core.services import WednesdayService  # noqa: F401 # see below for dependency injection

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
)


# FIXME this is confusing and high maintenance, but works for now while work on dependency injection and IoC
"""
Setup Dependency Injection
 - wireup singletons
 - import the source
 - reassign the import name to the singleton

This prevents the IDE from suggesting an import from the source, and suggests to use the singleton
"""

post_service: WednesdayService = app_module.provide_wednesday_service()
# add other singleton services here

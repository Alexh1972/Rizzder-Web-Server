import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class JobsConfig(AppConfig):
    name = 'rizzder_app.scheduler'

    def ready(self):
        from ..models import start
        logger.info("Starting scheduled jobs")
        start()
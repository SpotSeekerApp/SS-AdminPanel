from logtail.handler import LogtailHandler
import logging
import config

# logger
handler = LogtailHandler(source_token=config.LOGGER_SOURCE_TOKEN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)

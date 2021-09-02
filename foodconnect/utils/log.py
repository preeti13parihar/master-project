import sys
import logging
from django.conf import settings
from logmatic import JsonFormatter


def get_logger(name, level=settings.LOG_LEVEL):
    formatter = JsonFormatter(fmt="%(asctime) %(name) %(filename) %(funcName) %(levelname) %(lineno) %(message)", 
                                extra={"service": "loanmongers"})

    consolo_handler = logging.StreamHandler(stream=sys.stdout)
    consolo_handler.setLevel(level)
    consolo_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(consolo_handler)

    return logger


def validate_log_level(level):
    logging._checkLevel(level)
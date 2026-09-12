import sys
from loguru import logger
from config.settings import settings

def setup_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    return logger

setup_logger()

def get_logger(name: str):
    return logger.bind(name=name)
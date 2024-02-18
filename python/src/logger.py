import logging
import logging.config
from typing import Optional

logging.config.fileConfig("logging.conf")
logging.getLogger(__name__).debug("Configured logging")


def getLogger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name)

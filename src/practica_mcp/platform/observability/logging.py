"""Logging compartido.

IMPORTANTE con MCP por stdio: stdout es el canal del protocolo.
Nunca usar print(); los logs siempre van a stderr.
"""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        stream=sys.stderr,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

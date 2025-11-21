from __future__ import annotations

import logging
from typing import Optional
from colorama import Fore, Style, init

init(autoreset=True)

DEFAULT_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%dT%H:%M:%SZ"

LOG_COLORS = {
    logging.DEBUG: Fore.BLUE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_color = LOG_COLORS.get(record.levelno, "")
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


def init_logging(
    level: int,
    fmt: str = DEFAULT_FORMAT,
    datefmt: str = DEFAULT_DATEFMT,
) -> None:
    root = logging.getLogger()

    if getattr(root, "_configured", False):
        return

    root.setLevel(level)

    formatter = ColoredFormatter(fmt=fmt, datefmt=datefmt)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    setattr(root, "_configured", True)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name)


__all__ = ["get_logger", "init_logging"]

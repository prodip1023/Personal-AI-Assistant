import logging
import os
from datetime import datetime


def setup_logger(name: str = "Jarvis", level=logging.INFO) -> logging.Logger:
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"jarvis_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    formatter = logging.Formatter(
        "[ %(asctime)s ] %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

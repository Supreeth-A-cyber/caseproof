import logging
from pathlib import Path


def setup_logger():
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    logger = logging.getLogger("caseproof")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_directory / "caseproof.log",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
from pathlib import Path
import logging


def configure_logging(log_file: Path) -> None:
    logger = logging.getLogger("file_metadata")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return
    handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
    )
    logger.addHandler(handler)

def configure_logger_separator(log_file: Path) -> None:
    logger = logging.getLogger("separator")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return
    handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter(
            "%(message)s"
        )
    )
    logger.addHandler(handler)
from pathlib import Path
from collections.abc import Iterator
from datetime import datetime,timezone
import logging

from file_models import FileInfo
from file_scanner import scan_files

from logging_config import configure_logging,configure_logger_separator

configure_logging(Path("logs/scanner.log"))
configure_logger_separator(Path("logs/scanner.log"))

logger = logging.getLogger("file_metadata")
logger_sep = logging.getLogger("separator")

def scan_file_info(
    directory: Path,
    extensions: set[str] | None = None
) -> Iterator[FileInfo]:
    """Получает список файлов и метаданные по каждому"""
    logger_sep.info("=" * 100)

    files_found_count = 0
    files_processed_count = 0
    files_skipped_count = 0
    try:
        logger.info("Сканирование началось")
        for file in scan_files(directory, extensions):
            files_found_count += 1

            try:
                file_info = get_file_info(file)
            except FileNotFoundError:
                files_skipped_count += 1
                logger.warning("File %s not found", file)
                continue

            files_processed_count += 1
            yield file_info
    finally:
        logger.info(f"Сканирование завершено.")

    logger.info(
        "Найдено: %s | Обработано: %s | Пропущено: %s",
        files_found_count,
        files_processed_count,
        files_skipped_count
    )



def get_file_info(path: Path) -> FileInfo:
    """Получает метаданные файла"""
    if not path.exists():
        raise FileNotFoundError(
            f"Файл не существует: {path}"
        )

    if not path.is_file():
        raise IsADirectoryError(
            f"Ожидался файл: {path}"
        )
    info = path.stat()

    modified_at = datetime.fromtimestamp(
        info.st_mtime,
        tz=timezone.utc
    )

    return FileInfo(
        path=path,
        name=path.name,
        extension=path.suffix.lower(),
        size=info.st_size,
        modified_at=modified_at
    )


directory = Path("C://Users/coder/PycharmProjects/python-engineering-lab/testss")
files = scan_file_info(directory, {".py", ".txt"})


try:
    for f in files:
        print(f.name)
except FileNotFoundError as e:
    logger.error(e)




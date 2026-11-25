from pathlib import Path
from collections.abc import Iterator
from datetime import datetime,timezone
import logging

from file_models import FileInfo
from file_scanner import scan_files


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/metadata.log', level=logging.INFO)


def scan_file_info(
    directory: Path,
    extensions: set[str] | None = None
) -> Iterator[FileInfo]:
    """Получает список файлов и метаданные по каждому"""
    for file in scan_files(directory, extensions):
        try:
            yield get_file_info(file)
        except FileNotFoundError:
            logger.warning("File %s not found", file)


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


directory = Path("C://Users/coder/PycharmProjects/python-engineering-lab/tests")
files = scan_file_info(directory, {".py", ".txt"})

for f in files:
    print(f)


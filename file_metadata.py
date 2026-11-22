import sys
from pathlib import Path
from collections.abc import Iterator
from datetime import datetime,timezone

from file_models import FileInfo
from file_scanner import scan_files


def scan_file_info(
    directory: Path,
    extensions: set[str] | None = None
) -> Iterator[FileInfo]:
    """Получает список файлов и метаданные по каждому"""
    for file in scan_files(directory, extensions):
        yield get_file_info(file)


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


directory = Path("C://Users/artem/PycharmProjects/python-engineering-lab/tests")
files = scan_file_info(directory, {".py", ".txt"})

for f in files:
    print(f)


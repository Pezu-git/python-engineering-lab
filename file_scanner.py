from pathlib import Path
from collections.abc import Iterator
from file_models import FileInfo
from datetime import datetime,timezone


def scan_files(
    directory: Path,
    extensions: set[str] | None = None
) -> Iterator[Path]:
    if not directory.exists():
        raise FileNotFoundError(
            f"Директория не существует: {directory}"
        )
    if not directory.is_dir():
        raise NotADirectoryError(
            f"Не директория: {directory}"
        )
    if extensions is not None and not extensions:
        return
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        if extensions is None or path.suffix.lower() in extensions:
            yield path

# directory_path = Path("C:/Users/coder/PycharmProjects/python-engineering-lab/tests")
#
# try:
#     for file in scan_files(directory_path, {'.txt', '.csv', '.TXT', '.CSV', '.py'}):
#         print(file)
#
# except FileNotFoundError as error:
#     print(error)
#
# except NotADirectoryError as error:
#     print(error)


def get_file_info(path: Path) -> FileInfo:
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

search_file = Path("C:/Users/coder/PycharmProjects/python-engineering-lab/requirements.txt")

try:
    print(get_file_info(search_file))
except FileNotFoundError as error:
    print(error)
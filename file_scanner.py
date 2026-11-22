from pathlib import Path
from collections.abc import Iterator



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


# search_file = Path("C:/Users/coder/PycharmProjects/python-engineering-lab/requirements.txt")
#
# try:
#     print(get_file_info(search_file))
# except FileNotFoundError as error:
#     print(error)
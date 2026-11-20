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


directory_path = Path("C:/Users/coder/PycharmProjects/python-engineering-lab/tests")

try:
    for file in scan_files(directory_path, {'.txt', '.csv', '.TXT', '.CSV', '.py'}):
        print(file)

except FileNotFoundError as error:
    print(error)

except NotADirectoryError as error:
    print(error)
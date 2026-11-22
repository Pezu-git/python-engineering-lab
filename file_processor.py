from pathlib import Path

class UnsupportedFileFormatError(Exception):
    pass


def process_file(file_path: Path) -> str:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Файл не найден: {file_path}"
        )

    if file_path.is_dir():
        raise IsADirectoryError(
            f"Указан каталог вместо файла: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Путь не указывает на обычный файл: {file_path}"
        )

    if file_path.suffix.lower() not in (".txt", ".csv"):
        raise UnsupportedFileFormatError(
            f"Неподдерживаемый формат: {file_path.suffix}"
        )



    return f"Файл {file_path} готов к обработке"
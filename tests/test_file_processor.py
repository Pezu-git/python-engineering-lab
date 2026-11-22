
from pathlib import Path

import pytest

from file_processor import process_file, UnsupportedFileFormatError


def test_sample_files_count(sample_files: list[Path]):
    assert len(sample_files) == 3
    assert all(path.is_file() for path in sample_files)

def test_sample_files_processing(sample_files: list[Path]):
    for f in sample_files:
        if f.suffix.lower() == '.png':
            with pytest.raises(UnsupportedFileFormatError) as exc_info:
                process_file(f)
            assert "Неподдерживаемый формат: .png" in str(exc_info.value)
        else:
            assert process_file(f) == f"Файл {f} готов к обработке"


def test_missing_file():

    path = Path("definitely_missing_12345.txt")

    with pytest.raises(
        FileNotFoundError,
        match="Файл не найден:"
    ):
        process_file(path)

def test_directory_instead_of_file(tmp_path):

    dir_path = tmp_path

    with pytest.raises(
            IsADirectoryError,
            match="Указан каталог вместо файла"
    ):
        process_file(dir_path)


@pytest.mark.parametrize(
    "extension",
    [".img", ".png", ".exe", ".docx"]
)
def test_unsupported_format(tmp_path,extension):

    file_path = tmp_path / f"definitely_missing_12345{extension}"
    file_path.write_text("not valid format", encoding="utf-8")

    with pytest.raises(
        UnsupportedFileFormatError,
        match="Неподдерживаемый формат:"
    ):
        process_file(file_path)

@pytest.mark.parametrize(
    "extension",
    [".txt", ".csv", ".TXT", ".CSV"]
)
def test_valid_file(tmp_path, extension):

    file_path = tmp_path / f"validfile{extension}"
    file_path.write_text("valid file", encoding="utf-8")

    assert process_file(file_path) == f"Файл {file_path} готов к обработке"
import pytest
from pathlib import Path

from file_scanner import scan_files




def test_scan_files_recursive(tmp_path):
    """создаёт временную директорию с двумя файлами в корне и одним файлом во вложенной директории. Проверяет, что сканер нашёл все три файла."""
    (tmp_path / "first.txt").touch()
    (tmp_path / "second.csv").touch()

    subdirectory = tmp_path / "nested"
    subdirectory.mkdir()

    (subdirectory / "third.py").touch()

    files = scan_files(tmp_path)

    actual_names = {path.name for path in files}
    expected_names = {"first.txt", "second.csv", "third.py"}

    assert actual_names == expected_names


def test_scan_files_missing_directory(tmp_path):
    """проверяет выброс FileNotFoundError"""
    search_directory = tmp_path / "nested"
    with pytest.raises(FileNotFoundError):
        list(scan_files(search_directory))


def test_scan_files_not_directory(tmp_path):
    """проверяет выброс NotADirectoryError, если передать обычный файл."""
    search_file = tmp_path / "nested.md"
    search_file.touch()
    with pytest.raises(NotADirectoryError):
        list(scan_files(search_file))


@pytest.mark.parametrize(
    "extensions, expected_names",
    [
        (None, {"a.py", "b.txt", "c.csv", "d.PY"}),
        (set(), set()),
        ({".py"}, {"a.py", "d.PY"}),
        ({".txt", ".csv"}, {"b.txt", "c.csv"}),
    ],
)
def test_scan_files_filters(
    tmp_path: Path,
    extensions: set[str] | None,
    expected_names: set[str],
):

    for filename in ("a.py", "b.txt", "c.csv"):
        (tmp_path / filename).touch()

    sub = tmp_path / "sub"
    sub.mkdir()
    sub_f = sub / "d.PY"
    sub_f.touch()

    files = scan_files(tmp_path, extensions)
    actual_names = {path.name for path in files}

    assert actual_names == expected_names




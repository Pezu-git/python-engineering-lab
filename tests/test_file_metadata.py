from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

from file_metadata import scan_file_info
from file_models import FileInfo

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/metadatas.log', level=logging.INFO)

def test_scan_file_info(tmp_path):
    report_path = tmp_path / "report.txt"
    script_path = tmp_path / "script.py"

    report_path.touch()
    script_path.touch()

    report_path.write_text("This is a test")
    script_path.write_text("console.log('Hello World!')")


    result = list(scan_file_info(tmp_path, extensions={".py", ".txt"}))

    assert len(result) == 2

    assert all(isinstance(item, FileInfo) for item in result)
    
    for item in result:

        expected_text = "console.log('Hello World!')" if item.name == 'script.py' else "This is a test"
        expected_size = len(expected_text.encode("utf-8"))
        assert item.size == expected_size

        assert isinstance(item.modified_at, datetime), "modified_at должен быть datetime"
        assert item.modified_at.tzinfo is not None, "datetime должен иметь таймзону"
        assert item.modified_at.tzinfo == timezone.utc


def test_scan_file_info_one_missing(tmp_path, capsys, caplog):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    third = tmp_path / "third.txt"

    caplog.set_level(logging.WARNING, logger="file_metadata")

    first.touch()
    second.touch()
    third.touch()

    def mock_get_file_info(path: Path):
        if path.name == "second.txt":
            raise FileNotFoundError(f"Файл не существует: {path}")

        modified_at = datetime.fromtimestamp(
            path.stat().st_mtime,
            tz=timezone.utc
        )
        return FileInfo(
            path=path,
            name=path.name,
            extension=path.suffix.lower(),
            size=path.stat().st_size,
            modified_at=modified_at,
        )

    with patch("file_metadata.scan_files") as mocked_scan, patch("file_metadata.get_file_info", side_effect=mock_get_file_info) as mocked_info:

        mocked_scan.return_value = [first, second, third]

        results = list(scan_file_info(tmp_path))

        assert len(results) == 2
        assert results[0].name == "first.txt"
        assert results[1].name == "third.txt"

        assert mocked_info.call_count == 3

        record = caplog.records[0]

        assert record.levelname == "WARNING"
        assert "second.txt not found" in record.getMessage()


        # captured = capsys.readouterr()
        # assert "File" in captured.out
        # assert "second.txt" in captured.out
        # assert "not found" in captured.out


import pytest
from pathlib import Path
from datetime import datetime,timezone

from file_metadata import scan_file_info
from file_models import FileInfo


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

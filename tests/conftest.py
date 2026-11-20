from pathlib import Path
import pytest


@pytest.fixture
def sample_files(tmp_path: Path) -> list[Path]:
    fixfilenames = [
        "report.txt",
        "data.csv",
        "image.png",
    ]

    files = []

    for filename in fixfilenames:
        path = tmp_path / filename
        path.touch()
        files.append(path)

    return files
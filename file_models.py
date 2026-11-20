from datetime import datetime
from dataclasses import dataclass,FrozenInstanceError
from pathlib import Path


@dataclass(frozen=True)
class FileInfo:
    path: Path
    name: str
    extension: str
    size: int
    modified_at: datetime

timestamp = datetime.now()
file_info_a = FileInfo(
    path=Path("C:/Users/coder/PycharmProjects/python-engineering-lab/app.py"),
    name="app.py",
    extension=".py",
    size=1024,
    modified_at=timestamp
)
file_info_b = FileInfo(
    path=Path("C:/Users/coder/PycharmProjects/python-engineering-lab/app.py"),
    name="app.py",
    extension=".py",
    size=1024,
    modified_at=timestamp
)

print(file_info_a)
print(file_info_b)
print(file_info_a == file_info_b)

try:
    file_info_a.size = 2048
except FrozenInstanceError as e:
    print(type(e).__name__)
    print(e)


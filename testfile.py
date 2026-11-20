from pathlib import Path
from datetime import datetime, timezone

path = Path("file_models.py")

info = path.stat()

print(info)
print(info.st_size)
print(info.st_mtime)

modified_at = datetime.fromtimestamp(
    info.st_mtime,
    tz=timezone.utc
)
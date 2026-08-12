import hashlib
from pathlib import Path

def calculate_file_hash(
    file_path: Path
) -> str:sha256 = hashlib.sha256()

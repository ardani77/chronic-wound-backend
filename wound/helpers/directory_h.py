import os, sys
import shutil
from pathlib import Path

def create_folder(directory: str | Path) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

def delete_folder(directory: Path) -> None:
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory, ignore_errors=False)
        except PermissionError as e:
            print(f"Error Deleting Directory – {e.strerror}", file = sys.stderr)

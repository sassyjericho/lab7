import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path


class Database:
    """Conexiuni scurte, cu commit/rollback și închidere garantată."""

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        else:
            if getattr(sys, "frozen", False):
                exe_dir = Path(sys.executable).resolve().parent
                self.path = exe_dir / "data" / "animale.sqlite3"
                if not self.path.exists():
                    internal_db = exe_dir / "_internal" / "data" / "animale.sqlite3"
                    if internal_db.exists():
                        import shutil
                        self.path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(internal_db), str(self.path))
            else:
                self.path = Path(__file__).resolve().parent.parent / "data" / "animale.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def transaction(self):
        connection = sqlite3.connect(str(self.path), timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

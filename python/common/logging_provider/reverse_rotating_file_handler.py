import logging.handlers
import time
from pathlib import Path
from typing import Optional

class ReverseRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Do a rollover starting with .1, according to logviewer requirements."""

    def __init__(self, prefix, path, mode, max_bytes, backup_count, encoding='utf-8', delay=False):
        filename = f"{prefix}_{time.strftime('%d-%m-%Y')}_{time.strftime('%H-%M-%S')}"
        self.next_file_ext: int = 1
        dir_path = Path(path)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / filename
        super().__init__(str(file_path) + '.1', mode, max_bytes, backup_count, encoding, delay)
        self.baseFilename = str(file_path)

    def doRollover(self):
        """increase log file extension by +1"""
        if self.stream:
            self.stream.close()
            self.stream: Optional[any] = None
        if self.backupCount > 0:
            self.next_file_ext += 1
            if self.next_file_ext > self.backupCount:
                self.next_file_ext = 1
        if not self.delay:
            self.stream = open(f'{self.baseFilename}.{str(self.next_file_ext)}', 'w', encoding=self.encoding)

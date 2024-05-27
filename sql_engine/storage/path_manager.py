from pathlib import Path

from ..config.config import Config

class PathManager:
    def __init__(self) -> None:
        self.data_path = Config().data_path

    def get_data_path(self):
        return self.data_path

    def get_write_ahead_log_path(self, table: str):
        return self.data_path / table / 'writeahead.log'
    
    def get_sstables_path(self, table: str) -> Path:
        return self.data_path / table / 'sstables'
        
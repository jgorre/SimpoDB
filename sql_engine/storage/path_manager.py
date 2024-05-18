from ..constants import DATA_PATH

class PathManager:
    def get_write_ahead_log_path(self, table: str):
        return DATA_PATH / table / 'writeahead.log'
        
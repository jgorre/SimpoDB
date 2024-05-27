from pathlib import Path

class Config:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self, config: dict):
        if self.initialized:
            raise RuntimeError('Config is immutable and has already been initialized.')
        
        self.data_path = Path(config['dataPath'])
        self.initialized = True


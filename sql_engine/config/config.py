class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.database_url = "sqlite:///:memory:"
        self.debug = True

    # Customize stuff here

    def set(self, key, value):
        setattr(self, key, value)

    def get(self, key):
        return getattr(self, key, None)

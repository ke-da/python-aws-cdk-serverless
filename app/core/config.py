import os

class Settings:
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    def __init__(self):
        self.POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
        self.POSTGRES_USER = os.getenv('POSTGRES_USER')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        self.POSTGRES_DB = os.getenv('POSTGRES_DB')

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql://%s:%s@%s:%s/%s" % (
            self.POSTGRES_USER, self.POSTGRES_PASSWORD,
            self.POSTGRES_SERVER, self.POSTGRES_PORT, self.POSTGRES_DB)

    class Config:
        case_sensitive = True

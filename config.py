from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Todo API"
    admin_email: str = "admin@example.com"
    items_per_page: int = 10

    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int
    mysql_db: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = (
        "postgresql+psycopg2://postgres:456123@localhost:5432/postgres"
    )
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"
    mail_username: str = "example@test.com"
    mail_password: str = "password"
    mail_from: str = "example@test.com"
    mail_port: int = 465
    mail_server: str = "smtp.test.com"
    redis_host: str = "localhost"
    redis_port: int = 6379
    cloudinary_name: str = "cloudinary name"
    cloudinary_api_key: str = "0000000000000"
    cloudinary_api_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()

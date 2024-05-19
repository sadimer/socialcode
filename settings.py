from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    path: str

    class Config:
        env_file = (".env.local", ".env")
        env_file_encoding = "utf-8"

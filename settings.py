from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    path_dir: str
    tmp_dir: str

    class Config:
        env_file = (".env.local", ".env")
        env_file_encoding = "utf-8"

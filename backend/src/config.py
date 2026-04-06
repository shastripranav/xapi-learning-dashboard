from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    frontend_url: str = "http://localhost:5173"
    data_mode: str = "demo"

    lrs_endpoint: str = ""
    lrs_username: str = ""
    lrs_password: str = ""

    db_path: str = "analytics_cache.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

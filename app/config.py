from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./expo.db"
    sql_echo: bool = False

    # Seguridad
    jwt_secret_key: str
    jwt_algoritmo: str = "HS256"
    jwt_expira_minutos: int = 5

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
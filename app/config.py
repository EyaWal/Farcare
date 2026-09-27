from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration centralisée de l'app, lue depuis les variables d'environnement (.env)."""

    database_url: str = "sqlite:///./farcare.db"
    app_env: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()

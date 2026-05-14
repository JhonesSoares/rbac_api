from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT (Apenas declare o tipo e o Pydantic busca do ambiente/env)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # App
    APP_ENV: str
    FIRST_ADMIN_EMAIL: str
    FIRST_ADMIN_PASSWORD: str
    FIRST_ADMIN_NAME: str

    # Configuração moderna para o Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Esta linha ignora o POSTGRES_USER e evita o erro antigo
    )


settings = Settings()

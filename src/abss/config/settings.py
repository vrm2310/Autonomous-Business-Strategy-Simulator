from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ABSS"
    app_env: str = "development"
    log_level: str = "INFO"

    max_debate_iterations: int = 6
    proposal_convergence_threshold: float = 0.01
    weighted_approval_threshold: float = 0.75

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_db: str = "abss_db"
    postgres_user: str = "postgres"
    postgres_password: str = ""

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )


settings = Settings()

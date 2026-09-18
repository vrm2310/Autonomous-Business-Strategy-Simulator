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


settings = Settings()

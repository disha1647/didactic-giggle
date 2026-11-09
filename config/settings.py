from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CachePilot"
    DEBUG: bool = True

    # LLM configuration
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_API_KEY: str = ""

    # Database configuration (we'll use this in a later phase)
    DATABASE_URL: str = "sqlite:///./data/cachepilot.db"

    # Cache configuration (for later phases)
    EXACT_CACHE_ENABLED: bool = True
    SEMANTIC_CACHE_ENABLED: bool = False
    CACHE_TTL: int = 3600
    SEMANTIC_CACHE_THRESHOLD: float = 0.90

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
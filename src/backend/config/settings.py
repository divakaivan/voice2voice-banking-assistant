import os

from functools import lru_cache

from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """Database configuration.

    Attributes:
        name: Database name.
        user: Database user.
        password: Database password.
        host: Database host.
        port: Database port.
    """

    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    host: str = os.getenv("DB_HOST")
    port: str = os.getenv("DB_PORT")

    @property
    def conninfo(self) -> str:
        """PostgreSQL connection string in libpq format."""

        return (
            f"dbname={self.name} "
            f"user={self.user} "
            f"password={self.password} "
            f"host={self.host} "
            f"port={self.port}"
        )


class EngineConfig(BaseSettings):
    """
    API keys for external services.

    Attributes:
        GROQ_API_KEY: Groq API authentication key.
        OPENAI_API_KEY: OpenAI API authentication key.
    """

    GROQ_API_KEY: str = os.environ["GROQ_API_KEY"]
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        database: Configuration for the database.
        engine: API keys.
    """

    database: DatabaseConfig = DatabaseConfig()
    engine: EngineConfig = EngineConfig()


@lru_cache
def get_settings() -> Settings:
    """Retrieve application settings.

    Returns:
        Application settings.
    """
    return Settings()


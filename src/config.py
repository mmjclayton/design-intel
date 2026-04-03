from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # LLM
    llm_provider: str = Field(default="claude", description="LLM provider: claude, openai, ollama")
    llm_model: str = Field(default="claude-sonnet-4-20250514")
    llm_max_tokens: int = Field(default=4096)
    llm_temperature: float = Field(default=0.3)

    # API Keys
    anthropic_api_key: str = Field(default="")
    openai_api_key: str = Field(default="")

    # Knowledge
    knowledge_retrieval_limit: int = Field(default=2000)
    retrieval_top_k: int = Field(default=5)
    vector_enabled: bool = Field(default=False)

    # Critique
    critique_severity_threshold: str = Field(default="low")
    critique_tone: str = Field(default="opinionated")

    # Output
    output_format: str = Field(default="markdown")
    output_directory: str = Field(default="./output")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

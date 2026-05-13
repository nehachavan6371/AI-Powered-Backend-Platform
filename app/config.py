"""Application Configuration"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    app_name: str = "AI-Powered Backend Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    workers: int = 4
    host: str = "0.0.0.0"
    port: int = 8000

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2000

    # Database
    database_url: str
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 40

    # JWT & Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_s3_bucket: str = "llm-documents"
    aws_eks_cluster: str = "llm-cluster"

    # GCP
    gcp_project_id: Optional[str] = None
    gcp_credentials_path: Optional[str] = None
    gcp_dataset_id: str = "llm_analytics"

    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_cache_ttl: int = 3600

    # Vector Store
    faiss_index_path: str = "./data/faiss_index"
    vector_dimension: int = 1536
    vector_index_type: str = "IVFFlat"
    vector_nprobe: int = 10

    # RAG
    rag_top_k: int = 5
    rag_chunk_size: int = 1000
    rag_chunk_overlap: int = 100
    rag_similarity_threshold: float = 0.7

    # Rate Limiting
    rate_limit_queries_per_minute: int = 60
    rate_limit_documents_per_hour: int = 100

    # Monitoring
    sentry_dsn: Optional[str] = None
    monitoring_enabled: bool = True
    prometheus_port: int = 8001

    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(f"App: {settings.app_name} v{settings.app_version}")
    print(f"Debug: {settings.debug}")
    print(f"Database: {settings.database_url}")

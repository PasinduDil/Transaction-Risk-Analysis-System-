from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    WEBHOOK_SECRET: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    
    # LLM Configuration
    GROQ_API_KEY: str
    GROQ_API_ENDPOINT: str
    GROQ_MODEL: str
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 500
    
    # Risk Analysis
    HIGH_RISK_COUNTRIES: List[str] = ["RU", "IR", "KP", "VE", "MM"]
    HIGH_RISK_THRESHOLD: float = 0.7
    REVIEW_THRESHOLD: float = 0.3
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "env_file_encoding": "utf-8"
    }
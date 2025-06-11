from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 项目信息
    PROJECT_NAME: str = "API测试平台"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "企业级API测试管理平台"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://apiuser:password@localhost:3306/api_test"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 测试配置
    TEST_TIMEOUT: int = 30
    MAX_CONCURRENT_TESTS: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 
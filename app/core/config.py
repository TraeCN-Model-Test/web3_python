"""
应用配置模块
负责加载和管理应用配置
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""
    
    # 模型配置
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_ignore_empty=True
    )
    
    # 应用基础配置
    app_name: str = "Web3 API Service"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Web3 配置
    # 使用以太坊主网的Infura端点作为示例
    infura_project_id: Optional[str] = None
    ethereum_rpc_url: str = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
    
    # API 配置
    api_prefix: str = "/api/v1"


# 创建全局配置实例
settings = Settings()

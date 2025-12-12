"""
FastAPI应用主入口
创建和配置FastAPI应用实例
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.web3 import router as web3_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    处理应用启动和关闭事件
    """
    # 启动事件
    print(f"{settings.app_name} v{settings.app_version} 启动中...")
    print("API文档地址: http://localhost:8002/docs")

    yield

    # 关闭事件
    print(f"{settings.app_name} 正在关闭...")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="一个简单的Web3 API服务，提供与以太坊区块链交互的功能",
    debug=settings.debug,
    lifespan=lifespan
)

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(web3_router, prefix=settings.api_prefix)


@app.get("/", tags=["root"])
async def root() -> dict:
    """
    根路径，返回API基本信息
    """
    return {
        "message": f"欢迎使用 {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs",
        "api_prefix": settings.api_prefix
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    处理favicon.ico请求，返回204状态码
    """
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=settings.debug
    )
    
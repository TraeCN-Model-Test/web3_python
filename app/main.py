"""
FastAPI应用主入口
创建和配置FastAPI应用实例
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
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
    print("API文档地址: http://localhost:8000/docs")

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

# 配置静态文件和模板
static_dir = Path(__file__).parent.parent / "static"
templates_dir = Path(__file__).parent.parent / "templates"

# 挂载静态文件目录
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

if templates_dir.exists():
    @app.get("/explorer", response_class=HTMLResponse, tags=["ui"])
    async def api_explorer():
        """
        API浏览器界面
        提供可视化的API接口测试界面
        """
        html_file = templates_dir / "index.html"
        return HTMLResponse(content=html_file.read_text(), status_code=200)


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    根路径，直接返回API Explorer界面
    """
    try:
        templates_dir = Path(__file__).parent.parent / "templates"
        index_path = templates_dir / "index.html"
        
        if not index_path.exists():
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Explorer界面文件不存在")
        
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"), status_code=200)
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"加载Explorer界面失败: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"加载界面失败: {str(e)}")


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
        port=8000,
        reload=settings.debug
    )
    
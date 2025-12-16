"""
Web3 API服务启动入口
"""
import uvicorn

if __name__ == "__main__":
    print("启动Web3 API服务...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,  # 使用8001端口避免冲突
        reload=True
    )

# Web3 API 服务

这是一个基于FastAPI的简单Web3 API服务，提供与以太坊区块链交互的基本功能。

## 功能特性

- 连接到以太坊主网
- 获取当前区块号
- 查询地址余额
- 获取当前Gas价格
- 获取链ID

## 安装和运行

### 前置要求

- Python 3.10+
- uv (Python包管理器)

### 安装依赖

```bash
uv install
```

### 运行服务

```bash
uv run python main.py
```

服务将在 http://localhost:8001 上启动。

## API端点

### 基础端点

- `GET /` - 获取API基本信息
- `GET /api/v1/hello` - HelloWorld端点
- `GET /api/v1/status` - 获取Web3连接状态

### Web3功能端点

- `GET /api/v1/block-number` - 获取当前区块号
- `GET /api/v1/balance/{address}` - 获取指定地址的ETH余额
- `GET /api/v1/gas-price` - 获取当前Gas价格
- `GET /api/v1/chain-id` - 获取当前链ID

### API文档

启动服务后，可以通过以下地址访问交互式API文档：

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 使用示例

### 获取当前区块号

```bash
curl http://localhost:8001/api/v1/block-number
```

### 查询地址余额

```bash
curl http://localhost:8001/api/v1/balance/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

### 获取Gas价格

```bash
curl http://localhost:8001/api/v1/gas-price
```

## 项目结构

```
web3_python/
├── app/
│   ├── api/          # API路由
│   ├── core/         # 核心配置
│   ├── models/       # 数据模型
│   ├── services/     # 业务逻辑服务
│   └── main.py       # FastAPI应用入口
├── main.py           # 项目启动入口
├── pyproject.toml    # 项目配置和依赖
└── README.md         # 项目说明
```

## 技术栈

- FastAPI - Web框架
- Web3.py - 以太坊交互库
- Uvicorn - ASGI服务器
- Pydantic - 数据验证和设置管理

## 注意事项

- 本项目使用公共RPC端点连接到以太坊主网
- 公共端点可能有请求频率限制
- 在生产环境中，建议使用专用的RPC服务提供商

## 许可证

MIT License
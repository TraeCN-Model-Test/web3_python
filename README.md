# Web3 API 服务

基于FastAPI的Web3 API服务，提供与以太坊区块链交互的基本功能。

## 功能特性

- 连接到以太坊主网
- 获取当前区块号
- 查询地址余额
- 获取当前Gas价格
- 获取链ID

## 快速开始

### 安装依赖

```bash
uv install
```

### 运行服务

```bash
uv run python run.py
```

服务将在 http://localhost:8001 上启动。

## API端点

- `GET /api/v1/block-number` - 获取当前区块号
- `GET /api/v1/balance/{address}` - 获取指定地址的ETH余额
- `GET /api/v1/gas-price` - 获取当前Gas价格
- `GET /api/v1/chain-id` - 获取当前链ID

### API文档

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 技术栈

- FastAPI - Web框架
- Web3.py - 以太坊交互库
- Pydantic - 数据验证和设置管理
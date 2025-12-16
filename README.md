# Web3 API

基于 FastAPI 的以太坊区块链 API 服务。

## 快速开始

```bash
# 安装依赖
uv install

# 启动服务
uv run python run.py
```

服务启动后：
- API 文档: http://localhost:8000/docs
- 浏览器界面: http://localhost:8000

## API 端点

- `GET /api/v1/hello` - 基础测试接口
- `GET /api/v1/status` - 获取连接状态
- `GET /api/v1/block-number` - 获取区块号
- `GET /api/v1/balance/{address}` - 查询余额
- `GET /api/v1/chain-id` - 获取链 ID
- `GET /api/v1/gas-price` - 获取 Gas 价格
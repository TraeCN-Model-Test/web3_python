"""
Web3 API路由
提供与以太坊区块链交互的API端点
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from app.services.web3_service import web3_service

router = APIRouter()


@router.get("/hello", tags=["web3"])
async def hello_world() -> Dict[str, str]:
    """
    Web3 HelloWorld 端点
    返回简单的欢迎消息
    """
    return {"message": "Hello from Web3 API Service!"}


@router.get("/status", tags=["web3"])
async def get_connection_status() -> Dict[str, Any]:
    """
    获取Web3连接状态
    """
    return {
        "connected": web3_service.is_connected,
        "message": "已连接到以太坊网络" if web3_service.is_connected else "未连接到以太坊网络"
    }


@router.get("/block-number", tags=["web3"])
async def get_current_block_number() -> Dict[str, Any]:
    """
    获取当前区块号
    """
    result = web3_service.get_block_number()
    
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result


@router.get("/balance/{address}", tags=["web3"])
async def get_address_balance(address: str) -> Dict[str, Any]:
    """
    获取指定地址的ETH余额
    
    Args:
        address: 以太坊地址
        
    Returns:
        包含余额信息的字典
    """
    result = web3_service.get_balance(address)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/chain-id", tags=["web3"])
async def get_chain_id() -> Dict[str, Any]:
    """
    获取当前连接的链ID
    """
    result = web3_service.get_chain_id()
    
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result


@router.get("/gas-price", tags=["web3"])
async def get_gas_price() -> Dict[str, Any]:
    """
    获取当前Gas价格
    """
    result = web3_service.get_gas_price()
    
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result
"""
Web3连接服务
负责与以太坊区块链交互
"""
from typing import Dict, Any, Optional
from web3 import Web3
from web3.exceptions import (
    TimeExhausted,
    BlockNotFound,
    Web3ValidationError,
    ProviderConnectionError,
    Web3Exception
)
import requests.exceptions


class Web3Service:
    """Web3服务类，处理与区块链的交互"""
    
    def __init__(self):
        """初始化Web3连接"""
        self.w3: Optional[Web3] = None
        self.is_connected = False
        self._connect()
    
    def _connect(self) -> None:
        """连接到以太坊网络"""
        # 设置请求超时时间
        timeout = 10  # 10秒超时
        
        # 尝试连接的RPC端点列表
        rpc_endpoints = [
            {
                "name": "Ankr",
                "url": "https://rpc.ankr.com/eth"
            },
            {
                "name": "PublicNode",
                "url": "https://ethereum.publicnode.com"
            },
            {
                "name": "Cloudflare",
                "url": "https://cloudflare-eth.com"
            }
        ]
        
        for endpoint in rpc_endpoints:
            try:
                print(f"正在尝试连接到 {endpoint['name']} RPC端点: {endpoint['url']}")
                self.w3 = Web3(Web3.HTTPProvider(endpoint['url'], request_kwargs={'timeout': timeout}))
                
                # 检查连接是否成功
                if self.w3.is_connected():
                    self.is_connected = True
                    print(f"成功连接到以太坊网络（{endpoint['name']}）")
                    # 获取链ID确认连接到正确的网络
                    chain_id = self.w3.eth.chain_id
                    print(f"当前链ID: {chain_id}")
                    return
                else:
                    print(f"连接到 {endpoint['name']} 失败，尝试下一个端点...")
            except (requests.exceptions.RequestException, ConnectionError, TimeExhausted, ProviderConnectionError) as e:
                print(f"连接到 {endpoint['name']} 时发生网络错误: {str(e)}")
                continue
            except Web3Exception as e:
                print(f"连接到 {endpoint['name']} 时发生Web3错误: {str(e)}")
                continue
        
        print("所有RPC端点连接尝试均失败")
        self.is_connected = False
    
    def get_block_number(self) -> Dict[str, Any]:
        """获取当前区块号"""
        if not self.is_connected or not self.w3:
            return {"error": "未连接到以太坊网络"}
        
        try:
            block_number = self.w3.eth.block_number
            return {
                "success": True,
                "block_number": block_number,
                "message": f"当前区块号: {block_number}"
            }
        except (TimeExhausted, ConnectionError, requests.exceptions.RequestException) as e:
            return {"error": f"网络请求失败: {str(e)}"}
        except BlockNotFound as e:
            return {"error": f"区块数据获取失败: {str(e)}"}
        except Web3Exception as e:
            return {"error": f"Web3操作失败: {str(e)}"}
    
    def get_balance(self, address: str) -> Dict[str, Any]:
        """获取指定地址的ETH余额"""
        if not self.is_connected or not self.w3:
            return {"error": "未连接到以太坊网络"}
        
        try:
            # 验证地址格式
            if not self.w3.is_address(address):
                return {"error": "无效的以太坊地址"}
            
            # 获取余额（单位是Wei）
            balance_wei = self.w3.eth.get_balance(address)
            # 转换为ETH
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            return {
                "success": True,
                "address": address,
                "balance_wei": str(balance_wei),
                "balance_eth": str(balance_eth),
                "message": f"地址 {address} 的余额为 {balance_eth} ETH"
            }
        except (TimeExhausted, ConnectionError, requests.exceptions.RequestException) as e:
            return {"error": f"网络请求失败: {str(e)}"}
        except Web3ValidationError as e:
            return {"error": f"地址验证失败: {str(e)}"}
        except Web3Exception as e:
            return {"error": f"Web3操作失败: {str(e)}"}
    
    def get_chain_id(self) -> Dict[str, Any]:
        """获取当前连接的链ID"""
        if not self.is_connected or not self.w3:
            return {"error": "未连接到以太坊网络"}
        
        try:
            chain_id = self.w3.eth.chain_id
            return {
                "success": True,
                "chain_id": chain_id,
                "message": f"当前链ID: {chain_id}"
            }
        except (TimeExhausted, ConnectionError, requests.exceptions.RequestException) as e:
            return {"error": f"网络请求失败: {str(e)}"}
        except Web3Exception as e:
            return {"error": f"Web3操作失败: {str(e)}"}
    
    def get_gas_price(self) -> Dict[str, Any]:
        """获取当前Gas价格"""
        if not self.is_connected or not self.w3:
            return {"error": "未连接到以太坊网络"}
        
        try:
            gas_price = self.w3.eth.gas_price
            gas_price_gwei = self.w3.from_wei(gas_price, 'gwei')
            
            return {
                "success": True,
                "gas_price_wei": str(gas_price),
                "gas_price_gwei": str(gas_price_gwei),
                "message": f"当前Gas价格: {gas_price_gwei} Gwei"
            }
        except (TimeExhausted, ConnectionError, requests.exceptions.RequestException) as e:
            return {"error": f"网络请求失败: {str(e)}"}
        except Web3Exception as e:
            return {"error": f"Web3操作失败: {str(e)}"}


# 创建全局Web3服务实例
web3_service = Web3Service()

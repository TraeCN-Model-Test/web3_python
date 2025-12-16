#!/usr/bin/env python3
"""
测试UI界面功能
验证API浏览器是否正常工作
"""
import requests
import json
from typing import Dict, Any

def test_api_endpoints():
    """
    测试所有API端点
    验证Web3 API服务的各个端点是否正常工作
    """
    base_url = "http://localhost:8000"
    api_prefix = "/api/v1"
    
    print("🚀 开始测试Web3 API服务...")
    
    # 测试根路径（现在直接返回HTML界面）
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 根路径测试通过: {response.status_code}")
        content_type = response.headers.get('content-type', '')
        if 'text/html' in content_type:
            print(f"   返回HTML界面，内容长度: {len(response.text)} 字符")
        else:
            print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"❌ 根路径测试失败: {e}")
    
    # 测试API浏览器界面
    try:
        response = requests.get(f"{base_url}/explorer")
        print(f"✅ API浏览器界面测试通过: {response.status_code}")
        print(f"   页面内容长度: {len(response.text)} 字符")
    except Exception as e:
        print(f"❌ API浏览器界面测试失败: {e}")
    
    # 测试各个API端点
    endpoints = [
        ("hello", "GET"),
        ("status", "GET"),
        ("block-number", "GET"),
        ("chain-id", "GET"),
        ("gas-price", "GET"),
    ]
    
    for endpoint, method in endpoints:
        try:
            url = f"{base_url}{api_prefix}/{endpoint}"
            response = requests.get(url)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} 端点测试通过")
                data = response.json()
                print(f"   响应预览: {str(data)[:100]}...")
            else:
                print(f"⚠️  {endpoint} 端点返回状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint} 端点测试失败: {e}")
    
    # 测试余额查询端点
    try:
        test_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f525Eb"
        url = f"{base_url}{api_prefix}/balance/{test_address}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"✅ 余额查询端点测试通过")
            data = response.json()
            print(f"   地址 {test_address[:10]}... 的余额: {data.get('balance', 'N/A')} ETH")
        else:
            print(f"⚠️  余额查询端点返回状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 余额查询端点测试失败: {e}")
    
    print("\n🎉 测试完成！")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔍 API浏览器: http://localhost:8000/explorer")
    print("📋 ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    test_api_endpoints()
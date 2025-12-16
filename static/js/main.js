/**
 * Web3 API Explorer - 主JavaScript文件
 * 处理所有交互逻辑和API调用
 */

// 全局配置
const API_BASE = '/api/v1';
let currentResponse = null;

/**
 * 初始化应用
 * 页面加载完成后执行初始化操作
 */
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Web3 API Explorer 初始化开始...');
    
    try {
        // 初始化深色模式切换
        initDarkMode();
        
        // 检查连接状态
        await checkConnection();
        console.log('连接状态检查完成');
        
        // 获取基础数据
        await fetchBasicData();
        console.log('基础数据获取完成');
        
        // 绑定事件监听器
        bindEventListeners();
        console.log('事件监听器绑定完成');
        
        // 设置定时刷新
        setupAutoRefresh();
        console.log('自动刷新设置完成');
        
        console.log('Web3 API Explorer 初始化完成');
    } catch (error) {
        console.error('初始化失败:', error);
        showError('应用初始化失败，请刷新页面重试');
    }
});

/**
 * 初始化深色模式功能
 */
function initDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const body = document.body;
    
    if (!darkModeToggle) {
        console.warn('深色模式切换按钮未找到');
        return;
    }
    
    darkModeToggle.addEventListener('click', () => {
        console.log('深色模式切换');
        body.classList.toggle('dark-mode');
        const icon = darkModeToggle.querySelector('i');
        
        if (body.classList.contains('dark-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            console.log('切换到深色模式');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            console.log('切换到浅色模式');
        }
    });
}

/**
 * 检查与后端的连接状态
 */
async function checkConnection() {
    console.log('正在检查连接状态...');
    
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        console.log('连接状态响应:', data);
        updateConnectionStatus(data.connected);
        return data.connected;
    } catch (error) {
        console.error('连接检查失败:', error);
        updateConnectionStatus(false);
        return false;
    }
}

/**
 * 更新连接状态显示
 * @param {boolean} connected - 是否已连接
 */
function updateConnectionStatus(connected) {
    console.log('更新连接状态显示:', connected ? '已连接' : '未连接');
    
    const statusElement = document.getElementById('connection-status');
    const connectionText = document.getElementById('connection-text');
    
    if (!statusElement || !connectionText) {
        console.warn('连接状态元素未找到');
        return;
    }
    
    if (connected) {
        statusElement.innerHTML = '<span class="w-4 h-4 bg-yellow-300 rounded-full mr-3 animate-pulse"></span><span class="drop-shadow-lg font-extrabold">已连接</span>';
        statusElement.className = 'inline-flex items-center px-6 py-3 rounded-full text-sm font-bold status-connected backdrop-blur-sm';
        connectionText.textContent = '已连接';
        connectionText.className = 'text-2xl font-bold text-emerald-700 mt-1 status-success';
    } else {
        statusElement.innerHTML = '<span class="w-4 h-4 bg-yellow-300 rounded-full mr-3"></span><span class="drop-shadow-lg font-extrabold">未连接</span>';
        statusElement.className = 'inline-flex items-center px-6 py-3 rounded-full text-sm font-bold status-disconnected backdrop-blur-sm';
        connectionText.textContent = '未连接';
        connectionText.className = 'text-2xl font-bold text-red-600 mt-1 status-error';
    }
}

/**
 * 获取基础数据显示
 */
async function fetchBasicData() {
    console.log('开始获取基础数据...');
    
    try {
        // 并行获取所有数据
        const [blockResponse, chainResponse, gasResponse] = await Promise.all([
            fetch(`${API_BASE}/block-number`),
            fetch(`${API_BASE}/chain-id`),
            fetch(`${API_BASE}/gas-price`)
        ]);
        
        // 处理区块号数据
        if (blockResponse.ok) {
            const blockData = await blockResponse.json();
            updateBlockDisplay(blockData.block_number);
            console.log('区块号更新完成:', blockData.block_number);
        } else {
            console.warn('获取区块号失败:', blockResponse.status);
        }
        
        // 处理链ID数据
        if (chainResponse.ok) {
            const chainData = await chainResponse.json();
            updateChainDisplay(chainData.chain_id);
            console.log('链ID更新完成:', chainData.chain_id);
        } else {
            console.warn('获取链ID失败:', chainResponse.status);
        }
        
        // 处理Gas价格数据
        if (gasResponse.ok) {
            const gasData = await gasResponse.json();
            updateGasDisplay(gasData.gas_price_gwei);
            console.log('Gas价格更新完成:', gasData.gas_price_gwei);
        } else {
            console.warn('获取Gas价格失败:', gasResponse.status);
        }
        
        // 更新时间显示
        updateLastUpdateTime();
        
    } catch (error) {
        console.error('获取基础数据失败:', error);
        showError('获取基础数据失败');
    }
}

/**
 * 更新区块号显示
 * @param {number} blockNumber - 区块号
 */
function updateBlockDisplay(blockNumber) {
    const currentBlockElement = document.getElementById('current-block');
    const blockNumberDisplayElement = document.getElementById('block-number-display');
    
    if (currentBlockElement) {
        currentBlockElement.textContent = blockNumber.toLocaleString();
    }
    
    if (blockNumberDisplayElement) {
        blockNumberDisplayElement.textContent = blockNumber.toLocaleString();
    }
}

/**
 * 更新链ID显示
 * @param {number} chainId - 链ID
 */
function updateChainDisplay(chainId) {
    const chainIdElement = document.getElementById('chain-id-display');
    if (chainIdElement) {
        chainIdElement.textContent = chainId;
    }
}

/**
 * 更新Gas价格显示
 * @param {string} gasPrice - Gas价格（Gwei）
 */
function updateGasDisplay(gasPrice) {
    const gasPriceElement = document.getElementById('gas-price-display');
    if (gasPriceElement) {
        gasPriceElement.textContent = `${gasPrice} Gwei`;
    }
}

/**
 * 更新最后更新时间
 */
function updateLastUpdateTime() {
    const lastUpdateElement = document.getElementById('last-update');
    if (lastUpdateElement) {
        lastUpdateElement.textContent = new Date().toLocaleTimeString('zh-CN');
    }
}

/**
 * 绑定事件监听器
 */
function bindEventListeners() {
    console.log('绑定事件监听器...');
    
    // 地址输入框回车事件
    const addressInput = document.getElementById('address-input');
    if (addressInput) {
        addressInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                console.log('地址输入框回车事件触发');
                testBalance();
            }
        });
    }
}

/**
 * 设置自动刷新
 */
function setupAutoRefresh() {
    console.log('设置自动刷新（30秒间隔）');
    
    // 每30秒自动刷新数据
    setInterval(async () => {
        console.log('执行自动刷新');
        await checkConnection();
        await fetchBasicData();
    }, 30000);
}

/**
 * 测试API端点
 * @param {string} endpoint - API端点名称
 * @param {string} responseTimeElementId - 响应时间显示元素ID
 */
async function testEndpoint(endpoint, responseTimeElementId = null) {
    console.log(`测试端点: ${endpoint}`);
    
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) {
        console.error('响应容器未找到');
        return;
    }
    
    const startTime = Date.now();
    
    // 显示加载状态
    responseContainer.innerHTML = '<div class="loading text-center text-gray-500"><i class="fas fa-spinner fa-spin text-4xl mb-4"></i><p>正在请求API...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/${endpoint}`);
        const data = await response.json();
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        
        console.log(`端点 ${endpoint} 响应成功，耗时: ${responseTime}ms`);
        
        // 存储当前响应数据
        currentResponse = {
            status: response.status,
            statusText: response.statusText,
            data: data,
            responseTime: responseTime,
            endpoint: endpoint
        };
        
        // 更新响应时间显示
        if (responseTimeElementId) {
            const responseTimeElement = document.getElementById(responseTimeElementId);
            if (responseTimeElement) {
                responseTimeElement.textContent = `${responseTime}ms`;
            }
        }
        
        // 显示响应结果
        displayResponse(currentResponse);
        
    } catch (error) {
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        
        console.error(`端点 ${endpoint} 请求失败:`, error);
        displayError(error, responseTime, endpoint);
    }
}

/**
 * 显示API响应结果
 * @param {Object} responseData - 响应数据对象
 */
function displayResponse(responseData) {
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) return;
    
    const statusClass = responseData.status >= 200 && responseData.status < 300 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
    
    responseContainer.innerHTML = `
        <div class="mb-6">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-4">
                    <span class="px-3 py-1 rounded-full text-sm font-medium ${statusClass}">
                        ${responseData.status} ${responseData.statusText}
                    </span>
                    <span class="text-sm text-gray-600">
                        <i class="fas fa-clock mr-1"></i>响应时间: ${responseData.responseTime}ms
                    </span>
                    <span class="text-sm text-gray-600">
                        <i class="fas fa-link mr-1"></i>${responseData.endpoint}
                    </span>
                </div>
            </div>
        </div>
        <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
            <pre class="language-json text-sm"><code>${JSON.stringify(responseData.data, null, 2)}</code></pre>
        </div>
    `;
    
    // 应用语法高亮
    const codeElement = responseContainer.querySelector('code');
    if (codeElement && window.Prism) {
        Prism.highlightElement(codeElement);
    }
}

/**
 * 显示错误信息
 * @param {Error} error - 错误对象
 * @param {number} responseTime - 响应时间
 * @param {string} endpoint - 端点名称
 */
function displayError(error, responseTime, endpoint) {
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) return;
    
    responseContainer.innerHTML = `
        <div class="bg-red-50 border border-red-200 rounded-lg p-6">
            <div class="flex items-center mb-4">
                <i class="fas fa-exclamation-triangle text-red-500 text-2xl mr-3"></i>
                <h4 class="text-lg font-semibold text-red-800">请求失败</h4>
            </div>
            <div class="text-red-700">
                <p class="font-medium mb-2">错误信息:</p>
                <p class="text-sm bg-red-100 rounded p-3">${error.message}</p>
            </div>
            <div class="mt-4 text-sm text-red-600">
                <p><i class="fas fa-clock mr-1"></i>响应时间: ${responseTime}ms</p>
                <p><i class="fas fa-link mr-1"></i>端点: ${endpoint}</p>
            </div>
        </div>
    `;
}

/**
 * 测试余额查询功能
 */
async function testBalance() {
    console.log('测试余额查询');
    
    const addressInput = document.getElementById('address-input');
    if (!addressInput) {
        console.error('地址输入框未找到');
        return;
    }
    
    const address = addressInput.value.trim();
    
    // 验证地址格式
    if (!address) {
        showError('请输入以太坊地址');
        return;
    }
    
    if (!address.match(/^0x[a-fA-F0-9]{40}$/)) {
        showError('请输入有效的以太坊地址格式');
        return;
    }
    
    console.log('查询地址余额:', address);
    await testEndpoint(`balance/${address}`, 'balance-response-time');
}

/**
 * 复制响应数据到剪贴板
 */
function copyResponse() {
    console.log('复制响应数据');
    
    if (!currentResponse) {
        showError('没有可复制的响应数据');
        return;
    }
    
    const textToCopy = JSON.stringify(currentResponse.data, null, 2);
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        console.log('响应数据已复制到剪贴板');
        showCopySuccess();
    }).catch(err => {
        console.error('复制失败:', err);
        showError('复制失败: ' + err.message);
    });
}

/**
 * 显示复制成功提示
 */
function showCopySuccess() {
    const copyBtn = document.querySelector('button[onclick="copyResponse()"]');
    if (!copyBtn) return;
    
    const originalHTML = copyBtn.innerHTML;
    const originalClasses = copyBtn.className;
    
    // 更新按钮状态
    copyBtn.innerHTML = '<i class="fas fa-check mr-2"></i>已复制';
    copyBtn.className = originalClasses.replace('bg-gray-600 hover:bg-gray-700', 'bg-green-600');
    
    // 2秒后恢复原状
    setTimeout(() => {
        copyBtn.innerHTML = originalHTML;
        copyBtn.className = originalClasses;
    }, 2000);
}

/**
 * 清除响应显示
 */
function clearResponse() {
    console.log('清除响应显示');
    
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) return;
    
    responseContainer.innerHTML = `
        <div class="text-center text-gray-500">
            <i class="fas fa-code text-6xl mb-4 opacity-20"></i>
            <p class="text-lg">点击任意端点的"测试"按钮来查看API响应</p>
            <p class="text-sm mt-2">支持语法高亮和JSON格式化</p>
        </div>
    `;
    
    currentResponse = null;
}

/**
 * 刷新所有数据
 */
async function refreshAllData() {
    console.log('刷新所有数据');
    
    const refreshBtn = document.querySelector('button[onclick="refreshAllData()"]');
    if (!refreshBtn) {
        console.error('刷新按钮未找到');
        return;
    }
    
    const icon = refreshBtn.querySelector('i');
    const originalHTML = refreshBtn.innerHTML;
    
    // 添加加载状态
    icon.classList.add('fa-spin');
    refreshBtn.disabled = true;
    
    try {
        // 并行执行刷新操作
        await Promise.all([
            checkConnection(),
            fetchBasicData()
        ]);
        
        console.log('数据刷新成功');
        
        // 显示成功状态
        refreshBtn.innerHTML = '<i class="fas fa-check mr-2"></i>刷新成功';
        refreshBtn.classList.remove('bg-blue-600', 'hover:bg-blue-700');
        refreshBtn.classList.add('bg-green-600');
        
        // 2秒后恢复原状
        setTimeout(() => {
            refreshBtn.innerHTML = originalHTML;
            refreshBtn.classList.remove('bg-green-600');
            refreshBtn.classList.add('bg-blue-600', 'hover:bg-blue-700');
            refreshBtn.disabled = false;
            icon.classList.remove('fa-spin');
        }, 2000);
        
    } catch (error) {
        console.error('数据刷新失败:', error);
        showError('数据刷新失败');
        
        // 恢复按钮状态
        refreshBtn.innerHTML = originalHTML;
        refreshBtn.disabled = false;
        icon.classList.remove('fa-spin');
    }
}

/**
 * 显示错误信息
 * @param {string} message - 错误信息
 */
function showError(message) {
    console.error('错误:', message);
    alert(message); // 简单的错误提示，可以根据需要改进
}

// 全局函数导出，供HTML调用
window.testEndpoint = testEndpoint;
window.testBalance = testBalance;
window.copyResponse = copyResponse;
window.clearResponse = clearResponse;
window.refreshAllData = refreshAllData;
// 测试登录流程和路由跳转
console.log('=== 测试登录流程 ===');

// 1. 测试登录API
async function testLogin() {
    console.log('1. 测试登录API...');
    
    try {
        const response = await fetch('http://localhost:8000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: 'admin123',
                password: 'admin123'
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('✅ 登录API测试成功');
            console.log('- 获取到token:', data.access_token ? '是' : '否');
            console.log('- 用户信息:', data.user ? '存在' : '不存在');
            return data.access_token;
        } else {
            console.log('❌ 登录API测试失败:', data);
            return null;
        }
    } catch (error) {
        console.log('❌ 登录API请求错误:', error.message);
        return null;
    }
}

// 2. 测试获取当前用户
async function testGetCurrentUser(token) {
    console.log('2. 测试获取当前用户...');
    
    try {
        const response = await fetch('http://localhost:8000/api/v1/auth/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('✅ 获取用户信息成功');
            console.log('- 用户名:', data.username);
            console.log('- 邮箱:', data.email);
            console.log('- 超级用户:', data.is_superuser);
            return true;
        } else {
            console.log('❌ 获取用户信息失败:', data);
            return false;
        }
    } catch (error) {
        console.log('❌ 获取用户信息请求错误:', error.message);
        return false;
    }
}

// 3. 测试前端页面可访问性
async function testFrontendPages() {
    console.log('3. 测试前端页面可访问性...');
    
    const pages = [
        { name: '登录页', url: 'http://localhost/login' },
        { name: '仪表盘', url: 'http://localhost/dashboard' },
        { name: '接口管理', url: 'http://localhost/apis' }
    ];
    
    for (const page of pages) {
        try {
            const response = await fetch(page.url);
            if (response.ok) {
                console.log(`✅ ${page.name} - 可访问`);
            } else {
                console.log(`❌ ${page.name} - HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ ${page.name} - 网络错误: ${error.message}`);
        }
    }
}

// 运行测试
async function runTests() {
    const token = await testLogin();
    
    if (token) {
        await testGetCurrentUser(token);
    }
    
    await testFrontendPages();
    
    console.log('\n=== 测试完成 ===');
    console.log('如果登录API成功但前端跳转有问题，请检查：');
    console.log('1. 浏览器开发者工具的控制台是否有错误');
    console.log('2. 网络面板查看登录请求是否成功');
    console.log('3. Vue DevTools查看路由状态和store状态');
    console.log('\n请访问: http://localhost/login 进行测试');
}

// 如果在Node.js环境中运行
if (typeof window === 'undefined') {
    // Node.js环境，使用fetch polyfill
    const { default: fetch } = await import('node-fetch');
    global.fetch = fetch;
}

runTests().catch(console.error); 
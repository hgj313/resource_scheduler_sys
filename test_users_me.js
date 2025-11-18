// 简单测试脚本，验证 /users/me 端点
const testUserMe = async () => {
  try {
    // 模拟从 localStorage 获取 token
    const token = localStorage.getItem('auth.token');
    
    if (!token) {
      console.log('❌ 没有找到认证令牌，请先登录');
      return;
    }
    
    console.log('🔑 找到令牌:', token.substring(0, 20) + '...');
    
    // 直接调用 API 测试
    const response = await fetch('http://localhost:8000/api/v1/users/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const userData = await response.json();
      console.log('✅ /users/me 端点响应成功:');
      console.log('用户信息:', userData);
      console.log('用户邮箱:', userData.email);
    } else {
      console.log('❌ /users/me 端点响应失败:', response.status, response.statusText);
      const errorText = await response.text();
      console.log('错误详情:', errorText);
    }
  } catch (error) {
    console.log('❌ 测试过程中发生错误:', error.message);
  }
};

// 执行测试
testUserMe();
import api from './api';

const TOKEN_KEY = 'auth.token';
const USER_KEY = 'auth.user';

export async function login(username, password) {
  const res = await api.post('/auth/login', { username, password });
  const { access_token, user } = res.data;
  window.localStorage.setItem(TOKEN_KEY, access_token);
  window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  return user;
}

export function logout() {
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
}

export async function getCurrentUser() {
  try {
    // 总是从 API 获取最新的用户信息（确保包含email）
    const response = await api.get('/users/me');
    const user = response.data;
    
    // 更新本地存储的用户信息（确保包含完整字段）
    window.localStorage.setItem(USER_KEY, JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('从API获取用户信息失败:', error);
    
    // API失败时尝试使用本地存储的数据（降级方案）
    const raw = window.localStorage.getItem(USER_KEY);
    if (raw) {
      console.warn('使用本地存储的可能不完整的用户信息');
      return JSON.parse(raw);
    }
    
    return null;
  }
}

export function isAuthenticated() {
  return !!window.localStorage.getItem(TOKEN_KEY);
}
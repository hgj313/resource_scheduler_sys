import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // 后端API基础URL
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage读取token，并附加到请求头
    const token = window.localStorage.getItem('auth.token');
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 404) {
      console.error('请求的资源未找到');
    } else if (error.response?.status === 500) {
      console.error('服务器内部错误');
    } else if (error.response?.status === 401) {
      console.warn('未认证或令牌失效，跳转登录');
      // 可选：跳转到登录页面
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    } else if (error.code === 'ECONNABORTED') {
      console.error('请求超时');
    } else {
      console.error('请求失败:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
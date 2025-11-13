import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // 后端API基础URL
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
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
    } else if (error.code === 'ECONNABORTED') {
      console.error('请求超时');
    } else {
      console.error('请求失败:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
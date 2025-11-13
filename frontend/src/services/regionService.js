import api from './api';

const regionService = {
  // 获取区域列表
  getAll: () => api.get('/regions'),
  
  // 获取区域详情
  getById: (id) => api.get(`/regions/${id}`),
  
  // 创建区域
  create: (regionData) => api.post('/regions', regionData),
  
  // 更新区域
  update: (id, regionData) => api.put(`/regions/${id}`, regionData),
  
  // 删除区域
  delete: (id) => api.delete(`/regions/${id}`),
};

export default regionService;
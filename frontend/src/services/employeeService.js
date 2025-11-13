import api from './api';

const employeeService = {
  // 获取员工列表
  getAll: () => api.get('/employees'),
  
  // 获取员工详情
  getById: (id) => api.get(`/employees/${id}`),
  
  // 创建员工
  create: (employeeData) => api.post('/employees', employeeData),
  
  // 更新员工
  update: (id, employeeData) => api.put(`/employees/${id}`, employeeData),
  
  // 删除员工
  delete: (id) => api.delete(`/employees/${id}`),
};

export default employeeService;
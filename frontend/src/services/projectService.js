import api from './api';

const projectService = {
  // 获取项目列表
  getAll: () => api.get('/projects'),
  
  // 获取项目详情
  getById: (id) => api.get(`/projects/${id}`),
  
  // 创建项目
  create: (projectData) => api.post('/projects', projectData),
  
  // 更新项目
  update: (id, projectData) => api.put(`/projects/${id}`, projectData),
  
  // 删除项目
  delete: (id) => api.delete(`/projects/${id}`),
  
  // 为项目指派员工
  assignEmployee: (projectId, assignmentData) => api.post(`/projects/${projectId}/assignments`, assignmentData),
  
  // 获取项目成员列表
  getMembers: (projectId) => api.get(`/projects/${projectId}/members`),
};

export default projectService;
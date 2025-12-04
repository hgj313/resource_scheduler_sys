import api from './api';

const projectService = {
  // 列出所有项目
  getAll: () => api.get('/projects/'),
  // 获取单个项目
  getOne: (projectId) => api.get(`/projects/${projectId}`),
  // 创建项目
  create: (projectData) => api.post('/projects/', projectData),
  // 更新项目
  update: (id, projectData) => api.put(`/projects/${id}`, projectData),
  // 删除项目
  delete: (id) => api.delete(`/projects/${id}`),
  // 为项目指派员工（拖拽或勾选后选择时间段）
  assignEmployee: (projectId, employeeId, start, end, userEmail) =>
    api.post(`/projects/${projectId}/assignments`, {
      employee_id: employeeId,
      start_time: start,
      end_time: end,
      user_email: userEmail,
    }),
  assignFenbao: (projectId, fenbaoId) =>
    api.post(`/projects/${projectId}/fenbao`, null, { params: { fenbao_id: fenbaoId } }),
  removeFenbao: (projectId, fenbaoId) =>
    api.delete(`/projects/${projectId}/fenbao`, { params: { fenbao_id: fenbaoId } }),
};

export default projectService;

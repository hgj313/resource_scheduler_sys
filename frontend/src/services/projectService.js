import api from './api';

const projectService = {
  // 列出所有项目
  getAll: () => api.get('/projects/'),
  // 获取单个项目
  getOne: (projectId) => api.get(`/projects/${projectId}`),
  // 为项目指派员工（拖拽或勾选后选择时间段）
  assignEmployee: (projectId, employeeId, start, end) =>
    api.post(`/projects/${projectId}/assignments`, {
      employee_id: employeeId,
      start_time: start,
      end_time: end,
    }),
};

export default projectService;
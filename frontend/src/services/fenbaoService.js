import api from './api';

const fenbaoService = {
  getAll: () => api.get('/fenbaos/'),
  getOne: (id) => api.get(`/fenbaos/${id}`),
  create: (data) => api.post('/fenbaos/', data),
  update: (id, data) => api.put(`/fenbaos/${id}`, data),
  delete: (id) => api.delete(`/fenbaos/${id}`),
  // 分包团队
  listTeams: () => api.get('/fenbaos/teams'),
  getTeam: (teamId) => api.get(`/fenbaos/teams/${teamId}`),
  createTeam: (team) => api.post('/fenbaos/teams', team),
  updateTeam: (teamId, updates) => api.put(`/fenbaos/teams/${teamId}`, updates),
  deleteTeam: (teamId) => api.delete(`/fenbaos/teams/${teamId}`),
  completeTeam: (teamId) => api.post(`/fenbaos/teams/${teamId}/complete`),
};

export default fenbaoService;

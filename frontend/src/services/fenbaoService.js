import api from './api';

const fenbaoService = {
  getAll: () => api.get('/fenbaos/'),
  getOne: (id) => api.get(`/fenbaos/${id}`),
  create: (data) => api.post('/fenbaos/', data),
  update: (id, data) => api.put(`/fenbaos/${id}`, data),
  delete: (id) => api.delete(`/fenbaos/${id}`),
};

export default fenbaoService;


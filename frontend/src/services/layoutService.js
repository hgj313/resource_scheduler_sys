import api from './api';

const layoutService = {
  getProjectLayout: (projectId) => api.get(`/layout/${projectId}`),
  postRegionLayout: (region, payload) => api.post(`/layout/${region || 'all'}`, payload),
};

export default layoutService;
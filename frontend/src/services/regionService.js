import api from './api';

const regionService = {
  getEmployeeStats: (regionName) => api.get(`/regions/${encodeURIComponent(regionName)}/employees`),
  getProjectCount: (regionName) => api.get(`/regions/${encodeURIComponent(regionName)}/projects`),
};

export default regionService;


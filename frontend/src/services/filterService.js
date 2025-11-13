import api from './api';

const filterService = {
  // 设置主时间轴
  setMainTimeline: (start, end) => api.put('/filters/main-timeline', null, { params: { start, end } }),
  
  // 设置副时间轴
  setSecondaryTimeline: (start, end) => api.put('/filters/secondary-timeline', null, { params: { start, end } }),
  
  // 根据主时间轴过滤项目
  filterProjects: () => api.get('/filters/projects'),
  
  // 根据副时间轴过滤员工
  filterEmployees: (region) => api.get('/filters/employees', { params: { region } }),
};

export default filterService;
import api from './api';

const toISO = (v) => {
  try { return new Date(v).toISOString(); } catch { return v; }
};

const filterService = {
  // 设置主时间轴（统一用 ISO 字符串）
  setMainTimeline: (start, end) => api.put('/filters/main-timeline', null, { params: { start: toISO(start), end: toISO(end) } }),
  
  // 设置副时间轴（统一用 ISO 字符串）
  setSecondaryTimeline: (start, end) => api.put('/filters/secondary-timeline', null, { params: { start: toISO(start), end: toISO(end) } }),
  
  // 根据主时间轴过滤项目
  filterProjects: (region) => api.get('/filters/projects', region ? { params: { region } } : {}),
  
  // 根据副时间轴过滤员工
  filterEmployees: (region) => api.get('/filters/employees', { params: { region } }),
};

export default filterService;

import React, { useState, useEffect } from 'react';
import projectService from '../services/projectService';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await projectService.getAll();
        setProjects(response.data);
        setLoading(false);
      } catch (error) {
        console.error('获取项目列表失败:', error);
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div>
      <h2>项目管理</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>项目名称</th>
            <th>项目价值</th>
            <th>区域</th>
            <th>开始时间</th>
            <th>结束时间</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project.id}>
              <td>{project.id}</td>
              <td>{project.name}</td>
              <td>{project.value}</td>
              <td>{project.region}</td>
              <td>{new Date(project.start_time).toLocaleDateString()}</td>
              <td>{new Date(project.end_time).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Projects;
import React from 'react';
import { Link } from 'react-router-dom';
import '../../App.css';

const Navigation = () => {
  return (
    <nav className="app-navigation">
      <ul>
        <li><Link to="/">仪表板</Link></li>
        <li><Link to="/employees">员工管理</Link></li>
        <li><Link to="/projects">项目管理</Link></li>
        <li><Link to="/regions">区域管理</Link></li>
        <li><Link to="/assignments">资源分配</Link></li>
      </ul>
    </nav>
  );
};

export default Navigation;
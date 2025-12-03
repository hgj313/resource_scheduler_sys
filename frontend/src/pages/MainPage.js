import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RegionCard from '../components/RegionCard';
import NotificationManager from '../components/NotificationManager';
import '../styles/main.css';
import { getCurrentUser, isAuthenticated, logout } from '../services/authService';

const REGIONS = [
  { id: 'sw', name: '西南区域' },
  { id: 'hz', name: '华中区域' },
  { id: 'hn', name: '华南区域' },
  { id: 'hd', name: '华东区域' },
];

const MainPage = () => {
  const navigate = useNavigate();
  const [hoveredId, setHoveredId] = useState(null);
  const authed = isAuthenticated();
  const user = getCurrentUser();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSwitchAccount = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      <NotificationManager userId={user?.id} />
      <div className="main-layout">
      <div className="main-left card">
        <div className="dashboard-panel">
          <div className="panel-section title">仪表盘</div>

          <div className="panel-section">
            <div className="panel-item">当前用户：{authed ? (user?.username || '-') : '未登录'}</div>
          </div>

          <div className="panel-row split">
            <div className="panel-item">职位：{user?.title || '-'}</div>
            <div className="panel-item">区域：{user?.region || '-'}</div>
          </div>

          <div className="panel-section">
            <button className="panel-button btn" onClick={() => navigate('/projects')}>项目列表</button>
          </div>

          <div className="panel-section">
            <button className="panel-button btn" onClick={() => navigate('/employees')}>员工列表</button>
          </div>

          <div className="panel-row split">
            <button className="panel-button btn" onClick={() => navigate('/manage-employees')}>员工管理</button>
            <button className="panel-button btn" onClick={() => navigate('/manage-projects')}>项目管理</button>
          </div>

          <div className="panel-row split">
            <button className="panel-button btn" onClick={() => navigate('/manage-fenbaos')}>分包管理</button>
            <button className="panel-button btn" onClick={() => navigate('/employees')}>员工列表</button>
          </div>

          <div className="panel-row split">
            <button className="panel-button btn" onClick={() => navigate('/assignments')}>派遣记录表</button>
            <button className="panel-button btn" onClick={() => navigate('/notifications')}>消息通知</button>
          </div>

          <div className="panel-row split">
            <button className="panel-button btn" onClick={handleSwitchAccount}>切换账户</button>
            <button className="panel-button btn" onClick={handleLogout}>退出登录</button>
          </div>
        </div>
      </div>

      <div className="main-right">
        <h2 className="page-title">战略业务聚集地</h2>
        <div className="region-card-grid two-cols">
          {REGIONS.map((r) => (
            <RegionCard
              key={r.id}
              name={r.name}
              hovered={hoveredId === r.id}
              onMouseEnter={() => setHoveredId(r.id)}
              onMouseLeave={() => setHoveredId(null)}
              onClick={() => navigate(`/region/${r.id}`)}
            />
          ))}
        </div>
      </div>
      </div>
    </>
  );
};

export default MainPage;

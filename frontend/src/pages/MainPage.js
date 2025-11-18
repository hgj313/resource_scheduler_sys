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
    <div className="main-layout">
      {/* 通知管理器组件 - 用于显示实时通知 */}
      <NotificationManager userId={user?.id} />
      
      <div className="main-left card">
        <h2>仪表盘</h2>
        <div className="user-info">
          <div>登录状态：{authed ? '已登录' : '未登录'}</div>
          {authed ? (
            <>
              <div>当前用户：{user?.username || '-'}</div>
              <div className="actions" style={{ marginTop: 8 }}>
                <button className="btn" onClick={handleLogout}>退出登录</button>
                <button className="btn" onClick={handleSwitchAccount} style={{ marginLeft: 8 }}>切换账户</button>
                <button className="btn btn-primary" onClick={() => navigate('/notifications')} style={{ marginLeft: 8 }}>
                  通知中心
                </button>
              </div>
            </>
          ) : (
            <div className="actions" style={{ marginTop: 8 }}>
              <button className="btn btn-primary" onClick={() => navigate('/login')}>去登录</button>
            </div>
          )}
        </div>
      </div>
      <div className="main-right">
        <h2 className="page-title">战略业务聚集地</h2>
        <div className="region-card-grid">
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
  );
};

export default MainPage;
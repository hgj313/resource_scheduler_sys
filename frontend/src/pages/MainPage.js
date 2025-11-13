import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RegionCard from '../components/RegionCard';
import '../styles/main.css';

const REGIONS = [
  { id: 'sw', name: '西南区域' },
  { id: 'hz', name: '华中区域' },
  { id: 'hn', name: '华南区域' },
  { id: 'hd', name: '华东区域' },
];

const MainPage = () => {
  const navigate = useNavigate();
  const [hoveredId, setHoveredId] = useState(null);

  return (
    <div className="main-layout">
      <div className="main-left card">
        <h2>仪表盘</h2>
        <div className="user-info">
          <div>当前用户：张三</div>
          <div>角色：调度管理员</div>
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
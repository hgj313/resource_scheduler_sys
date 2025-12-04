import React from 'react';
import '../styles/components/region-card.css';

const RegionCard = ({ name, hovered, onMouseEnter, onMouseLeave, onClick, stats }) => {
  const cls = `region-card ${hovered ? 'region-card--hovered' : 'region-card--normal'}`;
  return (
    <div className={cls} onMouseEnter={onMouseEnter} onMouseLeave={onMouseLeave} onClick={onClick}>
      <div className="region-card__name">{name}</div>
      {stats && (
        <div className="region-card__stats">
          <div>项目总数：{stats.projects ?? '-'}</div>
          <div>员工总数：{stats.employees?.total_employees ?? '-'}</div>
          <div>项目经理：{stats.employees?.pm_count ?? '-'}</div>
          <div>硬景工程师：{stats.employees?.hardscape_engineer_count ?? '-'}</div>
          <div>软景工程师：{stats.employees?.softscape_engineer_count ?? '-'}</div>
        </div>
      )}
    </div>
  );
};

export default RegionCard;

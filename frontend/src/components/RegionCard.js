import React from 'react';
import '../styles/components/region-card.css';

const RegionCard = ({ name, hovered, onMouseEnter, onMouseLeave, onClick }) => {
  const cls = `region-card ${hovered ? 'region-card--hovered' : 'region-card--normal'}`;
  return (
    <div className={cls} onMouseEnter={onMouseEnter} onMouseLeave={onMouseLeave} onClick={onClick}>
      <div className="region-card__name">{name}</div>
    </div>
  );
};

export default RegionCard;
import React, { useState } from 'react';
import '../styles/components/timeline.css';

const SCALE_OPTIONS_MAIN = [
  { value: 'quarter', label: '季度' },
  { value: 'month', label: '月' },
  { value: 'day', label: '日' },
];
const SCALE_OPTIONS_SUB = [
  { value: 'month', label: '月' },
  { value: 'week', label: '周' },
  { value: 'day', label: '日' },
  { value: 'hour', label: '小时' },
];

// 时间轴组件：仅提供时间单位设置与起止时间设置，不再显示刻度
const Timeline = ({ type = 'main', scale = 'month', onScaleChange, onSetTime }) => {
  const options = type === 'main' ? SCALE_OPTIONS_MAIN : SCALE_OPTIONS_SUB;
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');

  const canSubmit = Boolean(start && end);

  const handleSubmit = () => {
    if (!canSubmit) return;
    // 将时间原样传递，后端FastAPI支持ISO格式解析
    onSetTime && onSetTime(start, end);
  };

  return (
    <div className={`timeline timeline--${type}`}>
      <div className="timeline__controls">
        <span>{type === 'main' ? '主时间轴' : '副时间轴'}：</span>
        <select value={scale} onChange={(e) => onScaleChange && onScaleChange(e.target.value)}>
          {options.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <input
          type="datetime-local"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />
        <span>至</span>
        <input
          type="datetime-local"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />
        <button className="btn btn-primary" disabled={!canSubmit} onClick={handleSubmit}>
          设置时间
        </button>
      </div>
    </div>
  );
};

export default Timeline;
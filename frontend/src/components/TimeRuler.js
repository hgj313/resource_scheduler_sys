import React, { useMemo } from 'react';
import '../styles/components/time-ruler.css';

function addStep(date, scale, step) {
  const d = new Date(date.getTime());
  if (scale === 'quarter') d.setMonth(d.getMonth() + step * 3);
  else if (scale === 'month') d.setMonth(d.getMonth() + step);
  else if (scale === 'week') d.setDate(d.getDate() + step * 7);
  else if (scale === 'day') d.setDate(d.getDate() + step);
  else d.setHours(d.getHours() + step);
  return d;
}

function formatLabel(date, scale) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  const h = String(date.getHours()).padStart(2, '0');
  if (scale === 'quarter') return `${y} Q${Math.floor((date.getMonth()) / 3) + 1}`;
  if (scale === 'month') return `${y}-${m}`;
  if (scale === 'week') return `${y}-${m}-${d}`;
  if (scale === 'day') return `${m}-${d}`;
  return `${m}-${d} ${h}:00`;
}

function genTicks(start, end, scale, unitLengthPx, minTickPx) {
  const totalMs = end.getTime() - start.getTime();
  if (totalMs <= 0) return [];
  const baseSteps = { quarter: 1, month: 1, week: 1, day: 1, hour: 1 };
  let step = baseSteps[scale] || 1;
  const estimateCount = 12;
  let ticks = [];
  let current = new Date(start.getTime());
  while (current <= end) {
    const ratio = (current.getTime() - start.getTime()) / totalMs;
    const left = ratio * unitLengthPx;
    ticks.push({ left, label: formatLabel(current, scale) });
    current = addStep(current, scale, step);
  }
  const density = ticks.length > 1 ? (ticks[1].left - ticks[0].left) : unitLengthPx;
  if (density < minTickPx) {
    const factor = Math.ceil((minTickPx / Math.max(density, 1)));
    step *= factor;
    ticks = [];
    current = new Date(start.getTime());
    while (current <= end) {
      const ratio = (current.getTime() - start.getTime()) / totalMs;
      const left = ratio * unitLengthPx;
      ticks.push({ left, label: formatLabel(current, scale) });
      current = addStep(current, scale, step);
    }
  }
  return ticks;
}

const TimeRuler = ({ start, end, scale, unitLengthPx, minTickPx = 60 }) => {
  const ticks = useMemo(() => genTicks(start, end, scale, unitLengthPx, minTickPx), [start, end, scale, unitLengthPx, minTickPx]);
  return (
    <div className="time-ruler" style={{ width: unitLengthPx }}>
      {ticks.map((t, idx) => (
        <div key={idx} className="time-ruler__tick" style={{ left: t.left }}>
          <span className="time-ruler__label">{t.label}</span>
        </div>
      ))}
    </div>
  );
};

export default TimeRuler;
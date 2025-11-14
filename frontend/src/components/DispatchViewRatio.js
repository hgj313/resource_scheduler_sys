import React, { useMemo } from 'react';
import '../styles/components/dispatch-view.css';

function assignLanesByRatio(items) {
  const sorted = [...items].sort((a, b) => a.start_point_ratio - b.start_point_ratio);
  const lanes = [];
  sorted.forEach((it) => {
    const start = it.start_point_ratio;
    let placed = false;
    for (const lane of lanes) {
      const last = lane[lane.length - 1];
      const lastEnd = last.start_point_ratio + last.ratio;
      if (start >= lastEnd) {
        lane.push(it);
        placed = true;
        break;
      }
    }
    if (!placed) lanes.push([it]);
  });
  return lanes;
}

const DispatchViewRatio = ({ entries = [], width = 800, unitLengthPx }) => {
  const lanes = useMemo(() => assignLanesByRatio(entries), [entries]);
  const base = unitLengthPx || width;
  return (
    <div className="dispatch-view" style={{ width: base }}>
      {lanes.map((lane, idx) => (
        <div className="dispatch-view__lane" key={idx}>
          {lane.map((e) => {
            const left = Math.max(0, Math.min(1, e.start_point_ratio)) * base;
            const w = Math.max(0, Math.min(1, e.ratio)) * base;
            return (
              <div className="dispatch-view__item" key={e.id} style={{ left, width: w }} title={e.name}>
                <span>{e.name}</span>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default DispatchViewRatio;
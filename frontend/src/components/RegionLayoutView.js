import React, { useMemo } from 'react';
import '../styles/components/region-layout-view.css';

function assignLanesByRatio(items) {
  const sorted = [...items].sort((a, b) => a.start_point_ratio - b.start_point_ratio);
  const lanes = [];
  sorted.forEach((it) => {
    const start = it.start_point_ratio;
    const end = start + it.project_ratio;
    let placed = false;
    for (const lane of lanes) {
      const last = lane[lane.length - 1];
      const lastEnd = last.start_point_ratio + last.project_ratio;
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

const RegionLayoutView = ({ entries = [], width = 800, laneHeight = 28 }) => {
  const lanes = useMemo(() => assignLanesByRatio(entries), [entries]);
  return (
    <div className="region-layout-view" style={{ width }}>
      {lanes.map((lane, idx) => (
        <div className="region-layout-view__lane" key={idx} style={{ height: laneHeight }}>
          {lane.map((e) => {
            const left = Math.max(0, Math.min(1, e.start_point_ratio)) * width;
            const w = Math.max(0, Math.min(1, e.project_ratio)) * width;
            return (
              <div
                key={e.project_id}
                className="region-layout-view__item"
                style={{ left, width: w }}
                title={`${e.project_name}`}
              >
                <span>{e.project_name}</span>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default RegionLayoutView;
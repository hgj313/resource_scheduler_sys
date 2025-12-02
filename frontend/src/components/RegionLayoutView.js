import React, { useMemo } from 'react';
import '../styles/components/region-layout-view.css';
import ProjectCard from './ProjectCard';

function assignLanesByRatio(items) {
  const sorted = [...items].sort((a, b) => a.start_point_ratio - b.start_point_ratio);
  const lanes = [];
  sorted.forEach((it) => {
    const start = it.start_point_ratio;
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

const RegionLayoutView = ({ entries = [], width = 800, laneHeight = 84, unitLengthPx, projectsById = {}, onOpenProject, onDropAssign }) => {
  const lanes = useMemo(() => assignLanesByRatio(entries), [entries]);
  return (
    <div className="region-layout-view" style={{ width: unitLengthPx || width }}>
      {lanes.map((lane, idx) => (
        <div className="region-layout-view__lane" key={idx} style={{ height: laneHeight }}>
          {lane.map((e) => {
            const base = unitLengthPx || width;
            const left = Math.max(0, Math.min(1, e.start_point_ratio)) * base;
            const w = Math.max(0, Math.min(1, e.project_ratio)) * base;
            return (
              <div
                key={e.project_id}
                className="region-layout-view__item"
                style={{ left, width: w }}
                title={`${e.project_name}`}
              >
                <div style={{ pointerEvents: 'auto' }}>
                  <ProjectCard
                    project={projectsById[e.project_id] || { id: e.project_id, name: e.project_name, start: '', end: '' }}
                    onOpen={onOpenProject}
                    onDropAssign={(pid, emp) => onDropAssign && onDropAssign(pid, emp)}
                  />
                </div>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default RegionLayoutView;

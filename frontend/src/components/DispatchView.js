import React, { useMemo } from 'react';
import '../styles/components/dispatch-view.css';

function layoutLanes(assignments) {
  const parse = (s) => new Date(s).getTime();
  const sorted = [...assignments].sort((a, b) => parse(a.start) - parse(b.start));
  const lanes = [];
  sorted.forEach((a) => {
    const s = parse(a.start);
    const e = parse(a.end);
    let placed = false;
    for (const lane of lanes) {
      const last = lane[lane.length - 1];
      const lastEnd = parse(last.end);
      if (s >= lastEnd) {
        lane.push(a);
        placed = true;
        break;
      }
    }
    if (!placed) lanes.push([a]);
  });
  return lanes;
}

function toPercent(start, end, minTs, maxTs) {
  const total = maxTs - minTs;
  const left = ((start - minTs) / total) * 100;
  const width = ((end - start) / total) * 100;
  return { left: `${left}%`, width: `${width}%` };
}

const DispatchView = ({ assignments }) => {
  const lanes = useMemo(() => layoutLanes(assignments), [assignments]);
  const times = assignments.flatMap((a) => [new Date(a.start).getTime(), new Date(a.end).getTime()]);
  const minTs = Math.min(...times);
  const maxTs = Math.max(...times);

  return (
    <div className="dispatch-view">
      {lanes.map((lane, idx) => (
        <div className="dispatch-view__lane" key={idx}>
          {lane.map((a) => {
            const s = new Date(a.start).getTime();
            const e = new Date(a.end).getTime();
            const style = toPercent(s, e, minTs, maxTs);
            return (
              <div className="dispatch-view__item" key={a.id} style={style} title={`${a.name} ${a.start}~${a.end}`}>
                <span>{a.name}</span>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default DispatchView;
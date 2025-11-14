import React, { useEffect, useRef, useState } from 'react';
import TimeRuler from './TimeRuler';

const ScrollableLayout = ({ start, end, scale, zoom = 1, onZoomChange, height = 400, children }) => {
  const wrapRef = useRef(null);
  const [baseWidth, setBaseWidth] = useState(800);
  const [unitLengthPx, setUnitLengthPx] = useState(800);
  const [dragging, setDragging] = useState(false);
  const originRef = useRef({ x: 0, w: 800 });

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    const update = () => {
      const w = el.clientWidth || 800;
      setBaseWidth(w);
      setUnitLengthPx(Math.round(w * zoom));
    };
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, [zoom]);

  const onWheel = (e) => {
    const el = wrapRef.current;
    if (!el) return;
    if (e.ctrlKey) {
      e.preventDefault();
      el.scrollLeft += e.deltaY;
    }
  };

  const onPointerDown = (e) => {
    if (e.shiftKey) {
      e.preventDefault();
      setDragging(true);
      originRef.current = { x: e.clientX, w: unitLengthPx };
    }
  };
  const onPointerMove = (e) => {
    if (!dragging) return;
    const dx = e.clientX - originRef.current.x;
    const factor = 1 + dx / 300;
    const nextZoom = Math.max(0.5, Math.min(5, (originRef.current.w / baseWidth) * factor));
    onZoomChange && onZoomChange(nextZoom);
    setUnitLengthPx(Math.round(baseWidth * nextZoom));
  };
  const onPointerUp = () => setDragging(false);

  return (
    <div ref={wrapRef} style={{ overflow: 'auto', height }} onWheel={onWheel} onPointerDown={onPointerDown} onPointerMove={onPointerMove} onPointerUp={onPointerUp}>
      <TimeRuler start={start} end={end} scale={scale} unitLengthPx={unitLengthPx} />
      <div style={{ width: unitLengthPx }}>
        {typeof children === 'function' ? children({ unitLengthPx }) : children}
      </div>
    </div>
  );
};

export default ScrollableLayout;
import React, { useEffect, useRef } from 'react';
import EmployeeCard from './EmployeeCard';
import '../styles/components/employee-pool.css';

const EmployeePool = ({ employees, checkboxEnabled = false, selectedIds = [], onToggle, draggable = false, onDragStart }) => {
  const rowRef = useRef(null);

  useEffect(() => {
    const el = rowRef.current;
    if (!el) return;
    const onWheel = (e) => {
      if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) {
        el.scrollLeft += e.deltaY;
        e.preventDefault();
      }
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, []);

  return (
    <div className="employee-pool">
      <div className="employee-pool__row" ref={rowRef}>
        {employees.map((e) => (
          <EmployeeCard
            key={e.id}
            employee={e}
            checkboxEnabled={checkboxEnabled}
            checked={selectedIds.includes(e.id)}
            onToggle={onToggle}
            draggable={draggable}
            onDragStart={onDragStart}
          />
        ))}
      </div>
    </div>
  );
};

export default EmployeePool;
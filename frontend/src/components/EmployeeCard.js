import React from 'react';
import '../styles/components/employee-card.css';

const EmployeeCard = ({ employee, checkboxEnabled = false, checked = false, onToggle, draggable = false, onDragStart }) => {
  return (
    <div
      className="employee-card"
      title={`${employee.name}（${employee.role}）`}
      draggable={draggable}
      onDragStart={(e) => onDragStart && onDragStart(e, employee)}
    >
      <div className="employee-card__header">
        <div className="employee-card__name">{employee.name}</div>
        <div className="employee-card__role">{employee.role}</div>
      </div>
      <div className="employee-card__footer">
        <label className="employee-card__checkbox">
          <input
            type="checkbox"
            disabled={!checkboxEnabled}
            checked={checked}
            onChange={() => onToggle && onToggle(employee.id)}
          />
          可派遣
        </label>
      </div>
    </div>
  );
};

export default EmployeeCard;
import React from 'react';
import '../styles/components/project-card.css';

const ProjectCard = ({ project, onOpen, onDropAssign }) => {
  const onDoubleClick = () => onOpen && onOpen(project.id);
  const handleDragOver = (e) => {
    e.preventDefault();
  };
  const handleDrop = (e) => {
    e.preventDefault();
    try {
      const txt = e.dataTransfer.getData('application/json') || e.dataTransfer.getData('text/plain');
      const payload = txt ? JSON.parse(txt) : null;
      if (payload && onDropAssign) {
        onDropAssign(project.id, payload);
      }
    } catch (err) {
      // ignore parse error
    }
  };
  return (
    <div
      className="project-card"
      onDoubleClick={onDoubleClick}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      title={`${project.name}`}
    >
      <div className="project-card__name">{project.name}</div>
      <div className="project-card__meta">
        <span className="project-card__id">#{project.id}</span>
        <span className="project-card__dates">{project.start} ~ {project.end}</span>
      </div>
    </div>
  );
};

export default ProjectCard;
import React from 'react';
import ProjectCard from './ProjectCard';
import '../styles/components/project-pool.css';

const ProjectPool = ({ projects, onOpenProject, scale = 'month', onDropAssign }) => {
  return (
    <div className="project-pool">
      <div className="project-pool__ruler">时间刻度尺（{scale}）</div>
      <div className="project-pool__channels">
        {projects.map((p) => (
          <div key={p.id} className="project-pool__channel">
            <ProjectCard project={p} onOpen={onOpenProject} onDropAssign={onDropAssign} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProjectPool;
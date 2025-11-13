import React, { useMemo, useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Timeline from '../components/Timeline';
import filterService from '../services/filterService';
import EmployeePool from '../components/EmployeePool';
import projectService from '../services/projectService';
import DispatchView from '../components/DispatchView';
import Modal from '../components/Modal';
import '../styles/project.css';

const MOCK_ASSIGNMENTS = [
  { id: 1, name: '张三', start: '2025-11-01', end: '2025-11-05' },
  { id: 2, name: '李四', start: '2025-11-02', end: '2025-11-07' },
  { id: 3, name: '王五', start: '2025-11-03', end: '2025-11-08' },
  { id: 4, name: '小李', start: '2025-11-09', end: '2025-11-12' },
  { id: 5, name: '小王', start: '2025-11-14', end: '2025-11-17' },
];

const ProjectView = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [subScale, setSubScale] = useState('week');
  const [showModal, setShowModal] = useState(false);
  const [selectedIds, setSelectedIds] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [assignments, setAssignments] = useState(MOCK_ASSIGNMENTS);
  const [timeModalOpen, setTimeModalOpen] = useState(false);
  const [assignStart, setAssignStart] = useState('');
  const [assignEnd, setAssignEnd] = useState('');
  const [projectName, setProjectName] = useState('');

  // 恢复并持久化副时间轴刻度（确保在组件内部调用hooks）
  useEffect(() => {
    try {
      const s = window.localStorage.getItem('timeline.sub.scale');
      if (s) setSubScale(s);
    } catch {}
  }, []);
  useEffect(() => {
    try { window.localStorage.setItem('timeline.sub.scale', subScale); } catch {}
  }, [subScale]);

  // 加载项目名称并在标题显示
  useEffect(() => {
    const fetchProjectName = async () => {
      try {
        const resp = await projectService.getOne(projectId);
        setProjectName(resp.data?.name || String(projectId));
      } catch {
        setProjectName(String(projectId));
      }
    };
    fetchProjectName();
  }, [projectId]);

  const toggleSelect = (id) => {
    setSelectedIds((prev) => (
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    ));
  };

  const onConfirmAssign = () => {
    if (selectedIds.length === 0) return;
    setTimeModalOpen(true);
  };

  return (
    <div className="project-layout">
      <div className="project-topbar">
        <button className="btn" onClick={() => navigate(-1)}>返回区域界面</button>
        <h2 className="project-title">{projectName || projectId}</h2>
      </div>

      <div className="card">
        <Timeline
          type="sub"
          scale={subScale}
          onScaleChange={setSubScale}
          onSetTime={async (start, end) => {
            try {
              await filterService.setSecondaryTimeline(start, end);
              const resp = await filterService.filterEmployees();
              const list = (resp.data || []).map((e) => ({ id: e.id, name: e.name, role: e.position || '', region: e.region }));
              setEmployees(list);
            } catch (err) {
              console.error('设置副时间轴失败', err);
            }
          }}
        />
      </div>

      <div className="card project-info">
        <div>项目信息卡片（占位）</div>
        <button className="btn btn-primary btn-add-person" onClick={() => setShowModal(true)}>添加项目人员</button>
      </div>

      <div className="card">
        <DispatchView assignments={assignments} />
      </div>

      {showModal && (
        <Modal title="选择派遣人员" onClose={() => setShowModal(false)}>
          <EmployeePool
            employees={employees}
            checkboxEnabled={true}
            selectedIds={selectedIds}
            onToggle={toggleSelect}
          />
          <div style={{ textAlign: 'right', marginTop: 12 }}>
            <button className="btn" onClick={() => setShowModal(false)}>取消</button>
            <button className="btn btn-primary" onClick={onConfirmAssign} style={{ marginLeft: 8 }}>确定派遣</button>
          </div>
        </Modal>
      )}

      {timeModalOpen && (
        <Modal title="选择派遣时间段" onClose={() => setTimeModalOpen(false)}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <input type="datetime-local" value={assignStart} onChange={(e) => setAssignStart(e.target.value)} />
            <span>至</span>
            <input type="datetime-local" value={assignEnd} onChange={(e) => setAssignEnd(e.target.value)} />
          </div>
          <div style={{ textAlign: 'right', marginTop: 12 }}>
            <button className="btn" onClick={() => setTimeModalOpen(false)}>取消</button>
            <button
              className="btn btn-primary btn-time"
              style={{ marginLeft: 8 }}
              onClick={async () => {
                if (!assignStart || !assignEnd) return;
                try {
                  const s = new Date(assignStart).toISOString();
                  const e = new Date(assignEnd).toISOString();
                  for (const empId of selectedIds) {
                    await projectService.assignEmployee(Number(projectId), empId, s, e);
                    const name = employees.find((x) => x.id === empId)?.name || String(empId);
                    setAssignments((prev) => ([...prev, { id: Date.now() + Math.random(), name, start: s.slice(0, 10), end: e.slice(0, 10) }]));
                  }
                  setTimeModalOpen(false);
                  setShowModal(false);
                  setSelectedIds([]);
                } catch (err) {
                  console.error('派遣失败', err);
                }
              }}
            >
              确定派遣
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default ProjectView;
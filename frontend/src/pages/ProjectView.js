import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Timeline from '../components/Timeline';
import filterService from '../services/filterService';
import EmployeePool from '../components/EmployeePool';
import projectService from '../services/projectService';
import DispatchViewRatio from '../components/DispatchViewRatio';
import layoutService from '../services/layoutService';
import { getCurrentUser } from '../services/authService';
import ScrollableLayout from '../components/ScrollableLayout';
import Modal from '../components/Modal';
import NotificationManager from '../components/NotificationManager';
import '../styles/project.css';


const ProjectView = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [subScale, setSubScale] = useState('week');
  const [showModal, setShowModal] = useState(false);
  const [selectedIds, setSelectedIds] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [assignmentsRatio, setAssignmentsRatio] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [projectStartISO, setProjectStartISO] = useState('');
  const [projectEndISO, setProjectEndISO] = useState('');
  const [timeModalOpen, setTimeModalOpen] = useState(false);
  const [assignStart, setAssignStart] = useState('');
  const [assignEnd, setAssignEnd] = useState('');
  const [projectName, setProjectName] = useState('');
  const [conflictOpen, setConflictOpen] = useState(false);
  const [conflictInfo, setConflictInfo] = useState(null);

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
        if (resp.data?.start_time && resp.data?.end_time) {
          setProjectStartISO(resp.data.start_time);
          setProjectEndISO(resp.data.end_time);
        }
      } catch {
        setProjectName(String(projectId));
      }
    };
    fetchProjectName();
  }, [projectId]);

  // 初次进入页面或派遣后，拉取后端员工布局参数
  useEffect(() => {
    const fetchLayout = async () => {
      try {
        const resp = await layoutService.getProjectLayout(Number(projectId));
        const entries = (resp.data || []).map((x) => ({ id: x.id, name: x.name, start_point_ratio: x.start_point_ratio, ratio: x.ratio }));
        setAssignmentsRatio(entries);
      } catch (err) {
        // ignore
      }
    };
    fetchLayout();
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
        <ScrollableLayout
          start={projectStartISO ? new Date(projectStartISO) : new Date()}
          end={projectEndISO ? new Date(projectEndISO) : new Date()}
          scale={subScale}
          zoom={zoom}
          onZoomChange={setZoom}
          height={240}
        >
          {({ unitLengthPx }) => (
            <DispatchViewRatio entries={assignmentsRatio} unitLengthPx={unitLengthPx} />
          )}
        </ScrollableLayout>
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

      {/* 员工通知管理器 - 为每个员工建立WebSocket连接接收实时通知 */}
      {employees.map(employee => (
        <NotificationManager 
          key={employee.id}
          employeeId={employee.id}
          mode="employee"
        />
      ))}

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
                  const currentUser = await getCurrentUser();
                  const userEmail = currentUser ? currentUser.user_email : '';
                  const s = new Date(assignStart).toISOString();
                  const e = new Date(assignEnd).toISOString();
                  for (const empId of selectedIds) {
                    await projectService.assignEmployee(Number(projectId), empId, s, e, userEmail);
                  }
                  const layoutResp = await layoutService.getProjectLayout(Number(projectId));
                  const entries = (layoutResp.data || []).map((x) => ({ id: x.id, name: x.name, start_point_ratio: x.start_point_ratio, ratio: x.ratio }));
                  setAssignmentsRatio(entries);
                  setTimeModalOpen(false);
                  setShowModal(false);
                  setSelectedIds([]);
                } catch (err) {
                  const data = err?.response?.data;
                  if (err?.response?.status === 409 && data?.error === '派遣时间冲突') {
                    setConflictInfo(data);
                    setConflictOpen(true);
                  }
                }
              }}
            >
              确定派遣
            </button>
          </div>
        </Modal>
      )}

      {conflictOpen && (
        <Modal title={conflictInfo?.message || '派遣时间冲突'} onClose={() => setConflictOpen(false)}>
          <div style={{ marginBottom: 12 }}>
            <div>错误：{conflictInfo?.error}</div>
            <div>冲突数量：{conflictInfo?.conflict_count}</div>
            <div>建议：{conflictInfo?.suggestion}</div>
          </div>
          <div>
            {(conflictInfo?.conflict_detail || []).map((c) => (
              <div key={c.id} className="card" style={{ padding: 8, marginBottom: 8 }}>
                <div>记录ID：{c.id}</div>
                <div>项目ID：{c.project_id}</div>
                <div>开始：{c.conflict_start}</div>
                <div>结束：{c.conflict_end}</div>
              </div>
            ))}
          </div>
          <div style={{ textAlign: 'right' }}>
            <button className="btn" onClick={() => setConflictOpen(false)}>关闭</button>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default ProjectView;

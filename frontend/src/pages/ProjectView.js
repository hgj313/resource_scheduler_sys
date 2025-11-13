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
  const [projectInfo, setProjectInfo] = useState(null);

  const toDateStr = (iso) => {
    if (!iso) return '-';
    try { return new Date(iso).toISOString().slice(0, 10); } catch { return '-'; }
  };

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
        setProjectInfo(resp.data || null);
      } catch {
        setProjectName(String(projectId));
        setProjectInfo(null);
      }
    };
    fetchProjectName();
  }, [projectId]);

  // 拉取并映射项目派遣列表到可视化
  useEffect(() => {
    let mounted = true;
    const fetchAssignments = async () => {
      try {
        const resp = await projectService.getAssignments(Number(projectId));
        const list = (resp.data || []).map((r) => ({
          id: r.id,
          name: r.employee_name || `员工 ${r.employee_id}`,
          start: toDateStr(r.start_time),
          end: toDateStr(r.end_time),
        }));
        if (mounted) setAssignments(list);
      } catch (err) {
        console.error('拉取项目派遣列表失败', err);
        if (mounted) setAssignments([]);
      }
    };
    fetchAssignments();
    return () => { mounted = false; };
  }, [projectId]);

  // 轮询检测派遣变更并自动更新（每10秒）
  useEffect(() => {
    const intv = setInterval(async () => {
      try {
        const resp = await projectService.getAssignments(Number(projectId));
        const list = (resp.data || []).map((r) => ({
          id: r.id,
          name: r.employee_name || `员工 ${r.employee_id}`,
          start: toDateStr(r.start_time),
          end: toDateStr(r.end_time),
        }));
        setAssignments(list);
      } catch (err) {
        // 轮询失败时不打断页面，仅记录错误
        console.debug('轮询派遣列表失败', err);
      }
    }, 10000);
    return () => clearInterval(intv);
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
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, justifyContent: 'space-between' }}>
          <div style={{ flex: 1 }}>
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
          <button className="btn btn-primary btn-add-person" onClick={() => setShowModal(true)}>添加项目人员</button>
        </div>
      </div>

      <div className="card project-info">
        <div style={{ fontWeight: 600, marginBottom: 6 }}>项目信息</div>
        <div style={{ color: '#333', marginBottom: 8 }}>项目名称：{projectInfo?.name || projectName || '-'}</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
          <div>开始时间：{toDateStr(projectInfo?.start_time)}</div>
          <div>结束时间：{toDateStr(projectInfo?.end_time)}</div>
          <div>员工分配数量：{assignments?.length || 0}</div>
          <div>价值：{projectInfo?.value ?? '-'}</div>
          <div>区域：{projectInfo?.region ?? '-'}</div>
          <div>项目ID：{projectId}</div>
        </div>
      </div>

      <div className="card">
        {assignments && assignments.length > 0 ? (
          <DispatchView assignments={assignments} />
        ) : (
          <div style={{ padding: 8, color: '#666' }}>暂无派遣数据</div>
        )}
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
                  }
                  // 派遣成功后刷新后端真实派遣列表，自动重排
                  try {
                    const resp = await projectService.getAssignments(Number(projectId));
                    const list = (resp.data || []).map((r) => ({
                      id: r.id,
                      name: r.employee_name || `员工 ${r.employee_id}`,
                      start: toDateStr(r.start_time),
                      end: toDateStr(r.end_time),
                    }));
                    setAssignments(list);
                  } catch {}
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
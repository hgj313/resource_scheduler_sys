import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Timeline from '../components/Timeline';
import filterService from '../services/filterService';
import layoutService from '../services/layoutService';
import RegionLayoutView from '../components/RegionLayoutView';
import ScrollableLayout from '../components/ScrollableLayout';
import EmployeePool from '../components/EmployeePool';
import '../styles/region.css';
import projectService from '../services/projectService';
import Modal from '../components/Modal';
import { getCurrentUser } from '../services/authService';
import NotificationManager from '../components/NotificationManager';
import fenbaoService from '../services/fenbaoService';

const REGION_NAMES = {
  sw: '西南区域',
  hz: '华中区域',
  hn: '华南区域',
  hd: '华东区域',
};

// 工具：ISO日期转简短字符串
const toDateStr = (iso) => {
  try { return new Date(iso).toISOString().slice(0, 10); } catch { return '-'; }
};

const RegionView = () => {
  const { regionId } = useParams();
  const navigate = useNavigate();
  const [mainScale, setMainScale] = useState('month');
  const [subScale, setSubScale] = useState('week');
  const [enableProjectRegionFilter, setEnableProjectRegionFilter] = useState(true);
  const [enableEmployeeRegionFilter, setEnableEmployeeRegionFilter] = useState(true);
  const [filterRegion, setFilterRegion] = useState(REGION_NAMES[regionId] || '');
  const [projects, setProjects] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [fenbaos, setFenbaos] = useState([]);
  const [regionLayoutEntries, setRegionLayoutEntries] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [mainStartISO, setMainStartISO] = useState('');
  const [mainEndISO, setMainEndISO] = useState('');
  const [secondaryReady, setSecondaryReady] = useState(false);
  const [assignModalOpen, setAssignModalOpen] = useState(false);
  const [assignTarget, setAssignTarget] = useState({ projectId: null, employee: null });
  const [assignStart, setAssignStart] = useState('');
  const [assignEnd, setAssignEnd] = useState('');
  const [conflictOpen, setConflictOpen] = useState(false);
  const [conflictInfo, setConflictInfo] = useState(null);

  // 读取并持久化时间轴刻度（必须在组件内部调用hooks）
  useEffect(() => {
    try {
      const m = window.localStorage.getItem('timeline.main.scale');
      const s = window.localStorage.getItem('timeline.sub.scale');
      if (m) setMainScale(m);
      if (s) setSubScale(s);
    } catch {}
  }, []);

  useEffect(() => {
    try { window.localStorage.setItem('timeline.main.scale', mainScale); } catch {}
  }, [mainScale]);

  useEffect(() => {
    try { window.localStorage.setItem('timeline.sub.scale', subScale); } catch {}
  }, [subScale]);

  // 当员工区域过滤变化且副时间轴已设置时，联动刷新员工
  useEffect(() => {
    const fetchEmployees = async () => {
      if (!secondaryReady) return;
      try {
        const resp = await filterService.filterEmployees(enableEmployeeRegionFilter ? filterRegion : undefined);
        const list = (resp.data || []).map((e) => ({ id: e.id, name: e.name, role: e.position || '', region: e.region }));
        setEmployees(list);
      } catch (err) {
        console.error('刷新员工失败', err);
      }
    };
    fetchEmployees();
  }, [enableEmployeeRegionFilter, filterRegion, secondaryReady]);

  // 当项目区域过滤或区域选择变化，且主时间轴已设置时，联动刷新项目与区域布局
  useEffect(() => {
    const refreshProjects = async () => {
      if (!mainStartISO || !mainEndISO) return;
      try {
        const resp = await filterService.filterProjects(enableProjectRegionFilter ? filterRegion : undefined);
        const list = (resp.data || []).map((p) => ({ id: p.id, name: p.name, start: p.start_time ? toDateStr(p.start_time) : '-', end: p.end_time ? toDateStr(p.end_time) : '-' }));
        setProjects(list);
        const payload = {
          project_id_list: list.map((p) => p.id),
          main_start_time: mainStartISO,
          main_end_time: mainEndISO,
        };
        const regionResp = await layoutService.postRegionLayout(enableProjectRegionFilter ? filterRegion : undefined, payload);
        const entries = (regionResp.data || []).map((x) => ({
          project_id: x.project_id,
          project_name: x.project_name,
          start_point_ratio: x.start_point_ratio,
          project_ratio: x.project_ratio ?? x.layout_ratio,
        }));
        setRegionLayoutEntries(entries);
      } catch (err) {
        console.error('刷新项目或区域布局失败', err);
      }
    };
    refreshProjects();
  }, [enableProjectRegionFilter, filterRegion, mainStartISO, mainEndISO]);

  useEffect(() => {
    const loadFenbaos = async () => {
      try {
        const resp = await fenbaoService.getAll();
        const list = (resp.data || []).map((f) => ({ id: f.id, name: f.name, professional: f.professional, staff_count: f.staff_count, level: f.level }));
        setFenbaos(list);
      } catch (err) {
        // ignore
      }
    };
    loadFenbaos();
  }, []);

  return (
    <div className="region-layout">
      <div className="region-topbar">
        <button className="btn" onClick={() => navigate('/main')}>返回主页面</button>
        <h2 className="region-title">{REGION_NAMES[regionId] || '区域'}</h2>
        <label style={{ marginLeft: 12 }}>
          <input
            type="checkbox"
            checked={enableProjectRegionFilter}
            onChange={(e) => setEnableProjectRegionFilter(e.target.checked)}
          />
          启用项目区域过滤
        </label>
      </div>

      <div className="card">
        <Timeline
          type="main"
          scale={mainScale}
          onScaleChange={setMainScale}
          onSetTime={async (start, end) => {
            try {
              await filterService.setMainTimeline(start, end);
              const resp = await filterService.filterProjects(enableProjectRegionFilter ? filterRegion : undefined);
              const list = (resp.data || []).map((p) => ({ id: p.id, name: p.name, start: p.start_time ? toDateStr(p.start_time) : '-', end: p.end_time ? toDateStr(p.end_time) : '-' }));
              setProjects(list);
              setMainStartISO(new Date(start).toISOString());
              setMainEndISO(new Date(end).toISOString());
              const payload = {
                project_id_list: list.map((p) => p.id),
                main_start_time: new Date(start).toISOString(),
                main_end_time: new Date(end).toISOString(),
              };
              const regionResp = await layoutService.postRegionLayout(enableProjectRegionFilter ? filterRegion : undefined, payload);
              const entries = (regionResp.data || []).map((x) => ({
                project_id: x.project_id,
                project_name: x.project_name,
                start_point_ratio: x.start_point_ratio,
                project_ratio: x.project_ratio ?? x.layout_ratio,
              }));
              setRegionLayoutEntries(entries);
            } catch (err) {
              console.error('设置主时间轴或拉取项目失败', err);
            }
          }}
        />
        <Timeline
          type="sub"
          scale={subScale}
          onScaleChange={setSubScale}
          onSetTime={async (start, end) => {
            try {
              await filterService.setSecondaryTimeline(start, end);
              const resp = await filterService.filterEmployees(enableEmployeeRegionFilter ? filterRegion : undefined);
              const list = (resp.data || []).map((e) => ({ id: e.id, name: e.name, role: e.position || '', region: e.region }));
              setEmployees(list);
              setSecondaryReady(true);
            } catch (err) {
              console.error('设置副时间轴或拉取员工失败', err);
            }
          }}
        />
      </div>

      <div className="card">
        <div className="employee-pool-header">
          <div>员工池：可用 {employees.length} 人</div>
          <div className="employee-pool-controls">
            <label>
              <input
                type="checkbox"
                checked={enableEmployeeRegionFilter}
                onChange={(e) => setEnableEmployeeRegionFilter(e.target.checked)}
              />
              启用员工区域过滤
            </label>
            <select
              disabled={!enableEmployeeRegionFilter}
              value={filterRegion}
              onChange={(e) => setFilterRegion(e.target.value)}
            >
              <option value="西南区域">西南区域</option>
              <option value="华中区域">华中区域</option>
              <option value="华南区域">华南区域</option>
              <option value="华东区域">华东区域</option>
            </select>
          </div>
        </div>
        <EmployeePool
          employees={employees}
          checkboxEnabled={false}
          draggable={true}
          onDragStart={(e, emp) => {
            try {
              e.dataTransfer.setData('application/json', JSON.stringify({ id: emp.id, name: emp.name }));
              e.dataTransfer.effectAllowed = 'copy';
            } catch {}
          }}
        />
      </div>

      <div className="card">
        <div className="employee-pool-header">
          <div>分包列表：共 {fenbaos.length} 个</div>
        </div>
        <div style={{ display:'grid', gap:8 }}>
          {(fenbaos || []).map((f) => (
            <div key={f.id} className="card" style={{ padding:8 }}>
              <div style={{ display:'flex', justifyContent:'space-between' }}>
                <strong>{f.name}</strong>
                <span>等级：{f.level}</span>
              </div>
              <div>专业：{f.professional}；人数：{f.staff_count}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <ScrollableLayout
          start={mainStartISO ? new Date(mainStartISO) : new Date()}
          end={mainEndISO ? new Date(mainEndISO) : new Date()}
          scale={mainScale}
          zoom={zoom}
          onZoomChange={setZoom}
          height={520}
        >
          {({ unitLengthPx }) => (
            <RegionLayoutView
              entries={regionLayoutEntries}
              unitLengthPx={unitLengthPx}
              projectsById={Object.fromEntries(projects.map((p) => [p.id, p]))}
              onOpenProject={(pid) => navigate(`/project/${pid}`)}
              onDropAssign={(pid, emp) => {
                setAssignTarget({ projectId: pid, employee: emp });
                setAssignStart('');
                setAssignEnd('');
                setAssignModalOpen(true);
              }}
            />
          )}
        </ScrollableLayout>
      </div>

      {assignModalOpen && (
        <Modal
          title={`派遣：${assignTarget.employee?.name} → 项目 ${assignTarget.projectId}`}
          onClose={() => setAssignModalOpen(false)}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <input type="datetime-local" value={assignStart} onChange={(e) => setAssignStart(e.target.value)} />
            <span>至</span>
            <input type="datetime-local" value={assignEnd} onChange={(e) => setAssignEnd(e.target.value)} />
          </div>
          <div style={{ textAlign: 'right', marginTop: 12 }}>
            <button className="btn" onClick={() => setAssignModalOpen(false)}>取消</button>
            <button
              className="btn btn-primary btn-time"
              onClick={async () => {
                if (!assignTarget.projectId || !assignTarget.employee || !assignStart || !assignEnd) return;
                try {
                  const currentUser = await getCurrentUser();
                  const userEmail = currentUser ? currentUser.user_email : '';
                  const s = new Date(assignStart).toISOString();
                  const e = new Date(assignEnd).toISOString();
                  await projectService.assignEmployee(assignTarget.projectId, assignTarget.employee.id, s, e, userEmail);
                  setAssignModalOpen(false);
                } catch (err) {
                  const data = err?.response?.data;
                  if (err?.response?.status === 409 && data?.error === '派遣时间冲突') {
                    setConflictInfo(data);
                    setConflictOpen(true);
                  }
                }
              }}
              style={{ marginLeft: 8 }}
            >
              确定派遣
            </button>
          </div>
        </Modal>
      )}

      {conflictOpen && (
        <Modal
          title={conflictInfo?.message || '派遣时间冲突'}
          onClose={() => setConflictOpen(false)}
        >
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

      {/* 员工通知管理器 - 为每个员工建立WebSocket连接接收实时通知 */}
      {employees.map(employee => (
        <NotificationManager 
          key={employee.id}
          employeeId={employee.id}
          mode="employee"
        />
      ))}
    </div>
  );
};

export default RegionView;

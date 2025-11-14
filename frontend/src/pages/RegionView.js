import React, { useEffect, useMemo, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Timeline from '../components/Timeline';
import filterService from '../services/filterService';
import layoutService from '../services/layoutService';
import RegionLayoutView from '../components/RegionLayoutView';
import ScrollableLayout from '../components/ScrollableLayout';
import EmployeePool from '../components/EmployeePool';
import ProjectPool from '../components/ProjectPool';
import '../styles/region.css';
import projectService from '../services/projectService';
import Modal from '../components/Modal';

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
  const [enableRegionFilter, setEnableRegionFilter] = useState(false);
  const [filterRegion, setFilterRegion] = useState(regionId);
  const [projects, setProjects] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [regionLayoutEntries, setRegionLayoutEntries] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [mainStartISO, setMainStartISO] = useState('');
  const [mainEndISO, setMainEndISO] = useState('');
  const [secondaryReady, setSecondaryReady] = useState(false);
  const [assignModalOpen, setAssignModalOpen] = useState(false);
  const [assignTarget, setAssignTarget] = useState({ projectId: null, employee: null });
  const [assignStart, setAssignStart] = useState('');
  const [assignEnd, setAssignEnd] = useState('');

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

  // 当区域过滤变化且副时间轴已设置时，联动刷新员工
  useEffect(() => {
    const fetchEmployees = async () => {
      if (!secondaryReady) return;
      try {
        const resp = await filterService.filterEmployees(enableRegionFilter ? filterRegion : undefined);
        const list = (resp.data || []).map((e) => ({ id: e.id, name: e.name, role: e.position || '', region: e.region }));
        setEmployees(list);
      } catch (err) {
        console.error('刷新员工失败', err);
      }
    };
    fetchEmployees();
  }, [enableRegionFilter, filterRegion, secondaryReady]);

  return (
    <div className="region-layout">
      <div className="region-topbar">
        <button className="btn" onClick={() => navigate('/main')}>返回主页面</button>
        <h2 className="region-title">{REGION_NAMES[regionId] || '区域'}</h2>
      </div>

      <div className="card">
        <Timeline
          type="main"
          scale={mainScale}
          onScaleChange={setMainScale}
          onSetTime={async (start, end) => {
            try {
              await filterService.setMainTimeline(start, end);
              const resp = await filterService.filterProjects();
              const list = (resp.data || []).map((p) => ({ id: p.id, name: p.name, start: p.start_time ? toDateStr(p.start_time) : '-', end: p.end_time ? toDateStr(p.end_time) : '-' }));
              setProjects(list);
              setMainStartISO(new Date(start).toISOString());
              setMainEndISO(new Date(end).toISOString());
              const payload = {
                project_id_list: list.map((p) => p.id),
                main_start_time: new Date(start).toISOString(),
                main_end_time: new Date(end).toISOString(),
              };
              const regionResp = await layoutService.postRegionLayout(enableRegionFilter ? filterRegion : undefined, payload);
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
              const resp = await filterService.filterEmployees(enableRegionFilter ? filterRegion : undefined);
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
                checked={enableRegionFilter}
                onChange={(e) => setEnableRegionFilter(e.target.checked)}
              />
              启用区域过滤
            </label>
            <select
              disabled={!enableRegionFilter}
              value={filterRegion}
              onChange={(e) => setFilterRegion(e.target.value)}
            >
              <option value="sw">西南</option>
              <option value="hz">华中</option>
              <option value="hn">华南</option>
              <option value="hd">华东</option>
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
        <ScrollableLayout
          start={mainStartISO ? new Date(mainStartISO) : new Date()}
          end={mainEndISO ? new Date(mainEndISO) : new Date()}
          scale={mainScale}
          zoom={zoom}
          onZoomChange={setZoom}
          height={260}
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
        <div style={{ marginTop: 12 }}>
          <ProjectPool
            projects={projects}
            onOpenProject={(pid) => navigate(`/project/${pid}`)}
            scale={mainScale}
            onDropAssign={(pid, emp) => {
              setAssignTarget({ projectId: pid, employee: emp });
              setAssignStart('');
              setAssignEnd('');
              setAssignModalOpen(true);
            }}
          />
        </div>
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
                  const s = new Date(assignStart).toISOString();
                  const e = new Date(assignEnd).toISOString();
                  await projectService.assignEmployee(assignTarget.projectId, assignTarget.employee.id, s, e);
                  setAssignModalOpen(false);
                } catch (err) {
                  console.error('派遣失败', err);
                }
              }}
              style={{ marginLeft: 8 }}
            >
              确定派遣
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default RegionView;
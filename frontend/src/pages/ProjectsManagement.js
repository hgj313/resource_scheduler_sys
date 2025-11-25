import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import projectService from '../services/projectService';

const ProjectsManagement = () => {
  const navigate = useNavigate();
  const regionOptions = ['西南区域','华中区域','华南区域','华东区域'];

  const [createForm, setCreateForm] = useState({ name:'', value:'', region:'', start_time:'', end_time:'' });
  const [updateForm, setUpdateForm] = useState({ name:'', value:'', region:'', start_time:'', end_time:'' });
  const [projects, setProjects] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [deleteId, setDeleteId] = useState('');
  const [messages, setMessages] = useState([]);

  const toISO = (v) => { try { return new Date(v).toISOString(); } catch { return v; } };

  const formatErrors = (err) => {
    const detail = err?.response?.data?.detail;
    if (Array.isArray(detail)) {
      return detail.map((d) => {
        const field = Array.isArray(d.loc) ? d.loc.join('.') : '';
        const msg = d.msg || '参数错误';
        return field ? `${field}: ${msg}` : msg;
      });
    }
    if (typeof detail === 'string') return [detail];
    return [err?.message || '请求失败'];
  };

  const onCreate = async (e) => {
    e.preventDefault();
    setMessages([]);
    try {
      const payload = {
        name: createForm.name,
        value: Number(createForm.value || 0),
        region: createForm.region || null,
        start_time: createForm.start_time ? toISO(createForm.start_time) : null,
        end_time: createForm.end_time ? toISO(createForm.end_time) : null,
      };
      await projectService.create(payload);
      setMessages(['创建成功']);
    } catch (err) {
      setMessages(formatErrors(err));
    }
  };

  const onUpdate = async (e) => {
    e.preventDefault();
    setMessages([]);
    try {
      const id = Number(selectedId);
      const payload = { ...updateForm };
      if (payload.value !== '') payload.value = Number(payload.value);
      if (payload.start_time) payload.start_time = new Date(payload.start_time).toISOString();
      if (payload.end_time) payload.end_time = new Date(payload.end_time).toISOString();
      await projectService.update(id, payload);
      setMessages(['更新成功']);
    } catch (err) {
      setMessages(formatErrors(err));
    }
  };

  const onDelete = async (e) => {
    e.preventDefault();
    setMessages([]);
    try {
      await projectService.delete(Number(deleteId));
      setMessages(['删除成功']);
    } catch (err) {
      setMessages(formatErrors(err));
    }
  };

  const onChangeCreate = (e) => {
    const { name, value } = e.target;
    setCreateForm((p) => ({ ...p, [name]: value }));
  };
  const onChangeUpdate = (e) => {
    const { name, value } = e.target;
    setUpdateForm((p) => ({ ...p, [name]: value }));
  };

  useEffect(() => {
    (async () => {
      try {
        const resp = await projectService.getAll();
        setProjects(resp.data || []);
      } catch {}
    })();
  }, []);

  const onSelectProject = (e) => {
    const id = e.target.value;
    setSelectedId(id);
    const p = projects.find((x) => String(x.id) === String(id));
    if (p) {
      const startIso = p.start_time ? new Date(p.start_time).toISOString().slice(0,16) : '';
      const endIso = p.end_time ? new Date(p.end_time).toISOString().slice(0,16) : '';
      setUpdateForm({
        name: p.name || '',
        value: String(p.value ?? ''),
        region: p.region || '',
        start_time: startIso,
        end_time: endIso,
      });
    } else {
      setUpdateForm({ name:'', value:'', region:'', start_time:'', end_time:'' });
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>项目管理</h2>
        {messages.length > 0 && (
          <div className="alert alert-success">
            {messages.map((m, i) => <div key={i}>{m}</div>)}
          </div>
        )}
        <div style={{ display:'grid', gap:16 }}>
          <div>
            <h3>创建项目</h3>
            <form onSubmit={onCreate}>
              <div className="form-group"><label>项目名称</label><input name="name" value={createForm.name} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>项目价值</label><input name="value" value={createForm.value} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>区域</label>
                <select name="region" value={createForm.region} onChange={onChangeCreate}>
                  <option value="">请选择</option>
                  {regionOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <div className="form-group"><label>开始时间</label><input type="datetime-local" name="start_time" value={createForm.start_time} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>结束时间</label><input type="datetime-local" name="end_time" value={createForm.end_time} onChange={onChangeCreate} /></div>
              <button className="btn btn-primary" type="submit">提交创建</button>
            </form>
          </div>

          <div>
            <h3>修改项目信息</h3>
            <form onSubmit={onUpdate}>
              <div className="form-group"><label>选择项目</label>
                <select value={selectedId} onChange={onSelectProject}>
                  <option value="">请选择项目</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>{p.id} - {p.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group"><label>项目名称</label><input name="name" value={updateForm.name} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>项目价值</label><input name="value" value={updateForm.value} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>区域</label>
                <select name="region" value={updateForm.region} onChange={onChangeUpdate}>
                  <option value="">不修改</option>
                  {regionOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <div className="form-group"><label>开始时间</label><input type="datetime-local" name="start_time" value={updateForm.start_time} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>结束时间</label><input type="datetime-local" name="end_time" value={updateForm.end_time} onChange={onChangeUpdate} /></div>
              <button className="btn btn-primary" type="submit">提交修改</button>
            </form>
          </div>

          <div>
            <h3>查询项目</h3>
            <button className="btn" onClick={() => navigate('/projects')}>打开项目列表</button>
          </div>

          <div>
            <h3>删除项目</h3>
            <form onSubmit={onDelete}>
              <div className="form-group"><label>项目ID</label><input value={deleteId} onChange={(e) => setDeleteId(e.target.value)} /></div>
              <button className="btn btn-danger" type="submit">确认删除</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectsManagement;

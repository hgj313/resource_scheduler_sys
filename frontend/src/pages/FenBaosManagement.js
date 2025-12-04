import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import fenbaoService from '../services/fenbaoService';

const FenBaosManagement = () => {
  const navigate = useNavigate();
  const [createForm, setCreateForm] = useState({ name:'', professional:'', staff_count:'', level:'' });
  const [updateForm, setUpdateForm] = useState({ name:'', professional:'', staff_count:'', level:'' });
  const [fenbaos, setFenbaos] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [deleteId, setDeleteId] = useState('');
  const [messages, setMessages] = useState([]);

  const load = async () => {
    const resp = await fenbaoService.getAll();
    setFenbaos(resp.data || []);
  };

  useEffect(() => { load(); }, []);

  const onChangeCreate = (e) => {
    const { name, value } = e.target;
    setCreateForm((s) => ({ ...s, [name]: value }));
  };
  const onChangeUpdate = (e) => {
    const { name, value } = e.target;
    setUpdateForm((s) => ({ ...s, [name]: value }));
  };

  const onCreate = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        name: createForm.name,
        professional: createForm.professional,
        staff_count: Number(createForm.staff_count) || 0,
        level: createForm.level,
      };
      await fenbaoService.create(payload);
      setMessages((m) => [...m, '分包创建成功']);
      setCreateForm({ name:'', professional:'', staff_count:'', level:'' });
      await load();
    } catch (err) {
      setMessages((m) => [...m, '分包创建失败']);
    }
  };

  const onUpdate = async (e) => {
    e.preventDefault();
    if (!selectedId) return;
    try {
      const payload = {
        name: updateForm.name || undefined,
        professional: updateForm.professional || undefined,
        staff_count: updateForm.staff_count ? Number(updateForm.staff_count) : undefined,
        level: updateForm.level || undefined,
      };
      await fenbaoService.update(Number(selectedId), payload);
      setMessages((m) => [...m, '分包更新成功']);
      setUpdateForm({ name:'', professional:'', staff_count:'', level:'' });
      setSelectedId('');
      await load();
    } catch (err) {
      setMessages((m) => [...m, '分包更新失败']);
    }
  };

  const onDelete = async (e) => {
    e.preventDefault();
    if (!deleteId) return;
    try {
      await fenbaoService.delete(Number(deleteId));
      setMessages((m) => [...m, '分包删除成功']);
      setDeleteId('');
      await load();
    } catch (err) {
      setMessages((m) => [...m, '分包删除失败']);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>分包管理</h2>
        {messages.length > 0 && (
          <div className="alert alert-success">
            {messages.map((m, i) => <div key={i}>{m}</div>)}
          </div>
        )}

        <div style={{ display:'grid', gap:16 }}>
          <div>
            <h3>创建分包</h3>
            <form onSubmit={onCreate}>
              <div className="form-group"><label>名称</label><input name="name" value={createForm.name} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>专业</label><input name="professional" value={createForm.professional} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>人数</label><input name="staff_count" value={createForm.staff_count} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>等级</label><input name="level" value={createForm.level} onChange={onChangeCreate} /></div>
              <button className="btn btn-primary" type="submit">提交创建</button>
            </form>
          </div>

          <div>
            <h3>更新分包</h3>
            <form onSubmit={onUpdate}>
              <div className="form-group"><label>选择ID</label>
                <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)}>
                  <option value="">请选择</option>
                  {fenbaos.map((f) => <option key={f.id} value={f.id}>{`${f.id} - ${f.name}`}</option>)}
                </select>
              </div>
              <div className="form-group"><label>名称</label><input name="name" value={updateForm.name} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>专业</label><input name="professional" value={updateForm.professional} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>人数</label><input name="staff_count" value={updateForm.staff_count} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>等级</label><input name="level" value={updateForm.level} onChange={onChangeUpdate} /></div>
              <button className="btn btn-primary" type="submit">提交更新</button>
            </form>
          </div>

          <div>
            <h3>删除分包</h3>
            <form onSubmit={onDelete}>
              <div className="form-group"><label>选择ID</label>
                <select value={deleteId} onChange={(e) => setDeleteId(e.target.value)}>
                  <option value="">请选择</option>
                  {fenbaos.map((f) => <option key={f.id} value={f.id}>{`${f.id} - ${f.name}`}</option>)}
                </select>
              </div>
              <button className="btn btn-danger" type="submit">删除</button>
            </form>
          </div>

          <div>
            <h3>查看分包列表</h3>
            <button className="btn" onClick={() => navigate('/fenbaos')}>分包列表页</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FenBaosManagement;

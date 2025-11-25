import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import employeeService from '../services/employeeService';

const EmployeesManagement = () => {
  const navigate = useNavigate();
  const regionOptions = ['西南区域','华中区域','华南区域','华东区域'];
  const positionOptions = ['项目经理','生产经理','成本经理','硬景主管','硬景技术工程师','硬景工程师','软景主管','软景工程师','成本控制工程师','采购工程师','内业工程师','实习生'];
  const departmentOptions = ['工程管理部','项目部','采购部'];

  const [createForm, setCreateForm] = useState({ name:'', email:'', phone:'', position:'', department:'', region:'' });
  const [updateForm, setUpdateForm] = useState({ name:'', email:'', phone:'', position:'', department:'', region:'' });
  const [employees, setEmployees] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [deleteId, setDeleteId] = useState('');
  const [messages, setMessages] = useState([]);

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
      await employeeService.create(createForm);
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
      await employeeService.update(id, payload);
      setMessages(['更新成功']);
    } catch (err) {
      setMessages(formatErrors(err));
    }
  };

  const onDelete = async (e) => {
    e.preventDefault();
    setMessages([]);
    try {
      await employeeService.delete(Number(deleteId));
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
        const resp = await employeeService.getAll();
        setEmployees(resp.data || []);
      } catch {}
    })();
  }, []);

  const onSelectEmployee = (e) => {
    const id = e.target.value;
    setSelectedId(id);
    const emp = employees.find((x) => String(x.id) === String(id));
    if (emp) {
      setUpdateForm({
        name: emp.name || '',
        email: emp.email || '',
        phone: emp.phone || '',
        position: emp.position || '',
        department: emp.department || '',
        region: emp.region || '',
      });
    } else {
      setUpdateForm({ name:'', email:'', phone:'', position:'', department:'', region:'' });
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>员工管理</h2>
        {messages.length > 0 && (
          <div className="alert alert-success">
            {messages.map((m, i) => <div key={i}>{m}</div>)}
          </div>
        )}
        <div style={{ display:'grid', gap:16 }}>
          <div>
            <h3>创建员工</h3>
            <form onSubmit={onCreate}>
              <div className="form-group"><label>姓名</label><input name="name" value={createForm.name} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>邮箱</label><input name="email" value={createForm.email} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>电话</label><input name="phone" value={createForm.phone} onChange={onChangeCreate} /></div>
              <div className="form-group"><label>职位</label>
                <select name="position" value={createForm.position} onChange={onChangeCreate}>
                  <option value="">请选择</option>
                  {positionOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <div className="form-group"><label>部门</label>
                <select name="department" value={createForm.department} onChange={onChangeCreate}>
                  <option value="">请选择</option>
                  {departmentOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <div className="form-group"><label>区域</label>
                <select name="region" value={createForm.region} onChange={onChangeCreate}>
                  <option value="">请选择</option>
                  {regionOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <button className="btn btn-primary" type="submit">提交创建</button>
            </form>
          </div>

          <div>
            <h3>修改员工信息</h3>
            <form onSubmit={onUpdate}>
              <div className="form-group"><label>选择员工</label>
                <select value={selectedId} onChange={onSelectEmployee}>
                  <option value="">请选择员工</option>
                  {employees.map((e) => (
                    <option key={e.id} value={e.id}>{e.id} - {e.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group"><label>姓名</label><input name="name" value={updateForm.name} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>邮箱</label><input name="email" value={updateForm.email} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>电话</label><input name="phone" value={updateForm.phone} onChange={onChangeUpdate} /></div>
              <div className="form-group"><label>职位</label>
                <select name="position" value={updateForm.position} onChange={onChangeUpdate}>
                  <option value="">不修改</option>
                  {positionOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <div className="form-group"><label>部门</label>
                <select name="department" value={updateForm.department} onChange={onChangeUpdate}>
                  <option value="">不修改</option>
                  {departmentOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <div className="form-group"><label>区域</label>
                <select name="region" value={updateForm.region} onChange={onChangeUpdate}>
                  <option value="">不修改</option>
                  {regionOptions.map((o) => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
              <button className="btn btn-primary" type="submit">提交修改</button>
            </form>
          </div>

          <div>
            <h3>查询员工</h3>
            <button className="btn" onClick={() => navigate('/employees')}>打开员工列表</button>
          </div>

          <div>
            <h3>删除员工</h3>
            <form onSubmit={onDelete}>
              <div className="form-group"><label>员工ID</label><input value={deleteId} onChange={(e) => setDeleteId(e.target.value)} /></div>
              <button className="btn btn-danger" type="submit">确认删除</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmployeesManagement;

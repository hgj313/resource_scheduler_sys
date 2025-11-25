import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import employeeService from '../services/employeeService';

const CreateEmployee = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    position: '',
    department: '',
    email: '',
    phone: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState([]);

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
    if (detail && typeof detail === 'object' && detail.message) return [detail.message];
    return [err?.message || '请求失败'];
  };

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setErrors([]);
    setSubmitting(true);
    try {
      await employeeService.create(form);
      navigate('/employees');
    } catch (err) {
      setErrors(formatErrors(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>新建员工</h2>
        {errors.length > 0 && (
          <div className="alert alert-error">
            {errors.map((e, i) => (
              <div key={i}>{e}</div>
            ))}
          </div>
        )}
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label>姓名</label>
            <input name="name" value={form.name} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>职位</label>
            <select name="position" value={form.position} onChange={onChange}>
              <option value="">请选择</option>
              {positionOptions.map((o) => (
                <option key={o} value={o}>{o}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>部门</label>
            <select name="department" value={form.department} onChange={onChange}>
              <option value="">请选择</option>
              {departmentOptions.map((o) => (
                <option key={o} value={o}>{o}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>邮箱</label>
            <input name="email" value={form.email} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>电话</label>
            <input name="phone" value={form.phone} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>区域</label>
            <select name="region" value={form.region || ''} onChange={onChange}>
              <option value="">请选择</option>
              {regionOptions.map((o) => (
                <option key={o} value={o}>{o}</option>
              ))}
            </select>
          </div>
          <button className="btn btn-primary" type="submit" disabled={submitting}>提交</button>
          <button className="btn" type="button" style={{ marginLeft: 8 }} onClick={() => navigate(-1)}>取消</button>
        </form>
      </div>
    </div>
  );
};

export default CreateEmployee;
  const regionOptions = ['西南区域','华中区域','华南区域','华东区域'];
  const positionOptions = ['项目经理','生产经理','成本经理','硬景主管','硬景技术工程师','硬景工程师','软景主管','软景工程师','成本控制工程师','采购工程师','内业工程师','实习生'];
  const departmentOptions = ['工程管理部','项目部','采购部'];

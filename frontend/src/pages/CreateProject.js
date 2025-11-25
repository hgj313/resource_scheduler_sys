import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import projectService from '../services/projectService';

const CreateProject = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    value: '',
    region: '',
    start_time: '',
    end_time: ''
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

  const toISO = (v) => {
    try {
      return new Date(v).toISOString();
    } catch {
      return v;
    }
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setErrors([]);
    setSubmitting(true);
    try {
      const payload = {
        name: form.name,
        value: form.value,
        region: form.region,
        start_time: form.start_time ? toISO(form.start_time) : null,
        end_time: form.end_time ? toISO(form.end_time) : null
      };
      await projectService.create(payload);
      navigate('/projects');
    } catch (err) {
      setErrors(formatErrors(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>新建项目</h2>
        {errors.length > 0 && (
          <div className="alert alert-error">
            {errors.map((e, i) => (
              <div key={i}>{e}</div>
            ))}
          </div>
        )}
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label>项目名称</label>
            <input name="name" value={form.name} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>项目价值</label>
            <input name="value" value={form.value} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>区域</label>
            <select name="region" value={form.region} onChange={onChange}>
              <option value="">请选择</option>
              {regionOptions.map((o) => (
                <option key={o} value={o}>{o}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>开始时间</label>
            <input type="datetime-local" name="start_time" value={form.start_time} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>结束时间</label>
            <input type="datetime-local" name="end_time" value={form.end_time} onChange={onChange} />
          </div>
          <button className="btn btn-primary" type="submit" disabled={submitting}>提交</button>
          <button className="btn" type="button" style={{ marginLeft: 8 }} onClick={() => navigate(-1)}>取消</button>
        </form>
      </div>
    </div>
  );
};

export default CreateProject;
  const regionOptions = ['西南区域','华中区域','华南区域','华东区域'];

import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../App.css';
import '../styles/login.css';
import { login } from '../services/authService';

const Login = () => {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(username, password);
      const from = location.state?.from?.pathname || '/main';
      navigate(from);
    } catch (err) {
      setError(err?.response?.data?.detail || '登录失败');
    }
  };

  return (
    <div className="login-page">
      <div className="login-card" role="dialog" aria-label="登录窗口">
        <div className="login-header">
          <h2 className="login-title">欢迎登录</h2>
          <p className="login-subtitle">人力资源协调系统</p>
        </div>
        <div className="login-body">
          <form onSubmit={handleSubmit} autoComplete="on">
            <div className="form-field">
              <label className="form-label" htmlFor="username">用户名</label>
              <input
                id="username"
                className="form-input"
                placeholder="请输入用户名"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="password">密码</label>
              <input
                id="password"
                type="password"
                className="form-input"
                placeholder="请输入密码"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {error && <div className="error-box">{error}</div>}
            <div className="login-actions">
              <button type="submit" className="btn-primary">登录</button>
            </div>
          </form>
        </div>
        <div className="login-footer">默认账户：admin / admin123</div>
      </div>
    </div>
  );
};

export default Login;
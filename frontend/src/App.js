import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Projects from './pages/Projects';
import Regions from './pages/Regions';
import Assignments from './pages/Assignments';
// 新增设计页面
import MainPage from './pages/MainPage';
import RegionView from './pages/RegionView';
import ProjectView from './pages/ProjectView';
import Login from './pages/Login';
import RequireAuth from './components/common/RequireAuth';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        
        <main className="app-main">
          <Routes>
            {/* 根路径显示登录界面 */}
            <Route path="/" element={<Login />} />
            {/* 登录别名 */}
            <Route path="/login" element={<Login />} />
            {/* 登录后的主页面 */}
            <Route path="/main" element={<RequireAuth><MainPage /></RequireAuth>} />
            {/* 保留原有仪表盘入口 */}
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/regions" element={<Regions />} />
            <Route path="/assignments" element={<Assignments />} />
            {/* 设计要求的区域与项目页面 */}
            <Route path="/region/:regionId" element={<RequireAuth><RegionView /></RequireAuth>} />
            <Route path="/project/:projectId" element={<RequireAuth><ProjectView /></RequireAuth>} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
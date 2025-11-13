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

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        
        <main className="app-main">
          <Routes>
            {/* 设计要求的主页 */}
            <Route path="/" element={<MainPage />} />
            {/* 保留原有仪表盘入口 */}
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/regions" element={<Regions />} />
            <Route path="/assignments" element={<Assignments />} />
            {/* 设计要求的区域与项目页面 */}
            <Route path="/region/:regionId" element={<RegionView />} />
            <Route path="/project/:projectId" element={<ProjectView />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
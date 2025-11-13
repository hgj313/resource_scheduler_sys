import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Header from './components/common/Header';
import Navigation from './components/common/Navigation';
import Footer from './components/common/Footer';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Projects from './pages/Projects';
import Regions from './pages/Regions';
import Assignments from './pages/Assignments';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Navigation />
        
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/regions" element={<Regions />} />
            <Route path="/assignments" element={<Assignments />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
import React, { useState, useEffect } from 'react';
import fenbaoService from '../services/fenbaoService';

const FenBaos = () => {
  const [fenbaos, setFenbaos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFenbaos = async () => {
      try {
        const response = await fenbaoService.getAll();
        setFenbaos(response.data || []);
      } catch (error) {
        console.error('获取分包列表失败:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchFenbaos();
  }, []);

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div>
      <h2>分包列表</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>专业</th>
            <th>人数</th>
            <th>可用人数</th>
            <th>等级</th>
          </tr>
        </thead>
        <tbody>
          {(fenbaos || []).map((f) => (
            <tr key={f.id}>
              <td>{f.id}</td>
              <td>{f.name}</td>
              <td>{f.professional}</td>
              <td>{f.staff_count}</td>
              <td>{f.available_staff_count ?? '-'}</td>
              <td>{f.level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FenBaos;


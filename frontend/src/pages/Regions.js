import React, { useState, useEffect } from 'react';
import regionService from '../services/regionService';

const Regions = () => {
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRegions = async () => {
      try {
        const response = await regionService.getAll();
        setRegions(response.data);
        setLoading(false);
      } catch (error) {
        console.error('获取区域列表失败:', error);
        setLoading(false);
      }
    };

    fetchRegions();
  }, []);

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div>
      <h2>区域管理</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>区域名称</th>
            <th>位置</th>
          </tr>
        </thead>
        <tbody>
          {regions.map((region) => (
            <tr key={region.id}>
              <td>{region.id}</td>
              <td>{region.name}</td>
              <td>{region.location}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Regions;
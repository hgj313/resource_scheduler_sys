import React, { useState, useEffect } from 'react';
import employeeService from '../services/employeeService';

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await employeeService.getAll();
        setEmployees(response.data);
        setLoading(false);
      } catch (error) {
        console.error('获取员工列表失败:', error);
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div>
      <h2>员工管理</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>姓名</th>
            <th>职位</th>
            <th>部门</th>
            <th>邮箱</th>
            <th>电话</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((employee) => (
            <tr key={employee.id}>
              <td>{employee.id}</td>
              <td>{employee.name}</td>
              <td>{employee.position}</td>
              <td>{employee.department}</td>
              <td>{employee.email}</td>
              <td>{employee.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Employees;
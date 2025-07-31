import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function DepartmentList() {
  const [departments, setDepartments] = useState([]);
  const location = useLocation();

  useEffect(() => {
    fetch('/api/departments')
      .then(res => res.json())
      .then(data => setDepartments(data.departments));
  }, []);

  return (
    <div>
      <h4>Departments</h4>
      <ul>
        {departments.map(dept => (
          <li key={dept.id}>
            <Link
              to={`/departments/${dept.id}`}
              style={{ fontWeight: location.pathname === `/departments/${dept.id}` ? 'bold' : 'normal' }}
            >
              {dept.name} ({dept.product_count})
            </Link>
          </li>
        ))}
        <li>
          <Link to="/">All Products</Link>
        </li>
      </ul>
    </div>
  );
}

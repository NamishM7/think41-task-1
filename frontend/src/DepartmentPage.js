import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function DepartmentPage() {
  const { id } = useParams();
  const [products, setProducts] = useState([]);
  const [deptName, setDeptName] = useState("");

  useEffect(() => {
    fetch(`/api/departments/${id}/products`)
      .then(res => res.json())
      .then(data => {
        setProducts(data.products);
        setDeptName(data.department);
      });
  }, [id]);

  return (
    <div>
      <h2>
        Department: {deptName} ({products.length} products)
      </h2>
      <Link to="/">View All Products</Link>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            <Link to={`/products/${product.id}`}>
              {product.name} — {product.brand}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

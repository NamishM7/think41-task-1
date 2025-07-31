import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  useEffect(() => {
    fetch(`/api/products/${id}`).then(res => res.json()).then(setProduct);
  }, [id]);
  if (!product) return <div>Loading...</div>;
  return (
    <div>
      <h2>{product.name} ({product.brand})</h2>
      <p>Category: {product.category}</p>
      <p>Price: ₹{product.retail_price}</p>
      <p>Department: {product.department}</p>
      <p>SKU: {product.sku}</p>
      <p>Distribution Center ID: {product.distribution_center_id}</p>
      <Link to="/">Back to Products</Link>
    </div>
  );
}

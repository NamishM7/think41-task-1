import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProductList from './src/ProductList';
import ProductDetail from './src/ProductDetail';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/products/:id" element={<ProductDetail />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;

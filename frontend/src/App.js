import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProductList from './ProductList';
import ProductDetail from './ProductDetail';
import DepartmentPage from './DepartmentPage';
import DepartmentList from './DepartmentList';

function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex' }}>
        {/* Left sidebar for departments */}
        <div style={{ width: '20%', minWidth: '150px' }}>
          <DepartmentList />
        </div>
        {/* Main content area */}
        <div style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<ProductList />} />
            <Route path="/products/:id" element={<ProductDetail />} />
            <Route path="/departments/:id" element={<DepartmentPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
export default App;

import React from "react";
import "./App.css";
import "./styles/artworld.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import HomePage from "./components/HomePage";
import GalleryPage from "./components/GalleryPage";
import ProductPage from "./components/ProductPage";
import CartPage from "./components/CartPage";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <main style={{ paddingTop: '80px' }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/gallery" element={<GalleryPage />} />
            <Route path="/print/:id" element={<ProductPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/about" element={<div className="container-artworld section-spacing"><h1 className="section-title text-center">About - Coming Soon</h1></div>} />
            <Route path="/contact" element={<div className="container-artworld section-spacing"><h1 className="section-title text-center">Contact - Coming Soon</h1></div>} />
          </Routes>
        </main>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
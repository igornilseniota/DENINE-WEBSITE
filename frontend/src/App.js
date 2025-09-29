import React from "react";
import "./App.css";
import "./styles/artworld.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import HomePage from "./components/HomePage";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <main style={{ paddingTop: '80px' }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/gallery" element={<div className="container-artworld section-spacing"><h1 className="section-title">Gallery - Coming Soon</h1></div>} />
            <Route path="/print/:id" element={<div className="container-artworld section-spacing"><h1 className="section-title">Product Page - Coming Soon</h1></div>} />
            <Route path="/about" element={<div className="container-artworld section-spacing"><h1 className="section-title">About - Coming Soon</h1></div>} />
            <Route path="/contact" element={<div className="container-artworld section-spacing"><h1 className="section-title">Contact - Coming Soon</h1></div>} />
            <Route path="/cart" element={<div className="container-artworld section-spacing"><h1 className="section-title">Cart - Coming Soon</h1></div>} />
          </Routes>
        </main>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
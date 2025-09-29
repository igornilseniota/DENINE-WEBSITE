import React from 'react';
import '../styles/artworld.css';

export const Footer = () => {
  return (
    <footer className="footer-artworld">
      <div className="container-artworld">
        <div className="footer-content">
          <div className="footer-section">
            <h4>DE---NINE</h4>
            <p>
              Premium fine art prints for modern spaces. Each piece is carefully curated and produced to museum standards.
            </p>
          </div>
          
          <div className="footer-section">
            <h4>Collections</h4>
            <a href="/gallery">Gallery</a>
            <a href="/about">About the Artist</a>
            <a href="/contact">Custom Orders</a>
          </div>
          
          <div className="footer-section">
            <h4>Support</h4>
            <a href="/contact">Contact Us</a>
            <a href="/shipping">Shipping Info</a>
            <a href="/returns">Returns</a>
            <a href="/care">Print Care</a>
          </div>
        </div>
        
        <div className="text-center mt-xl pt-lg" style={{borderTop: '1px solid #374151'}}>
          <p className="caption-text">
            © 2024 DE---NINE. All rights reserved. | Premium fine art prints, worldwide shipping.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
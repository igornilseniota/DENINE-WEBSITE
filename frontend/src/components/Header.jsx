import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/artworld.css';

export const Header = () => {
  const location = useLocation();

  return (
    <header className="header-artworld">
      <div className="container-artworld">
        <div className="header-content">
          <Link to="/" className="brand-text">
            DE---NINE
          </Link>
          
          <nav className="nav-menu">
            <Link 
              to="/" 
              className={`nav-link ${
                location.pathname === '/' ? 'text-black' : ''
              }`}
            >
              Home
            </Link>
            <Link 
              to="/gallery" 
              className={`nav-link ${
                location.pathname === '/gallery' ? 'text-black' : ''
              }`}
            >
              Gallery
            </Link>
            <Link 
              to="/about" 
              className={`nav-link ${
                location.pathname === '/about' ? 'text-black' : ''
              }`}
            >
              About
            </Link>
            <Link 
              to="/contact" 
              className={`nav-link ${
                location.pathname === '/contact' ? 'text-black' : ''
              }`}
            >
              Contact
            </Link>
            <Link 
              to="/cart" 
              className={`nav-link ${
                location.pathname === '/cart' ? 'text-black' : ''
              }`}
            >
              Cart
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
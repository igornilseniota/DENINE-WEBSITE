import React, { useState, useEffect } from 'react';
import AdminLogin from './AdminLogin';
import AdminDashboard from './AdminDashboard';

const AdminMain = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const adminAuth = localStorage.getItem('denine-admin');
    if (adminAuth === 'authenticated') {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="section-spacing">
        <div className="container-artworld text-center">
          <h1 className="section-title">Loading...</h1>
        </div>
      </div>
    );
  }

  return (
    <div>
      {isAuthenticated ? (
        <AdminDashboard onLogout={setIsAuthenticated} />
      ) : (
        <AdminLogin onLogin={setIsAuthenticated} />
      )}
    </div>
  );
};

export default AdminMain;
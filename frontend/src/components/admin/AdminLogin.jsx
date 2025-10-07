import React, { useState } from 'react';
import '../../styles/artworld.css';

const AdminLogin = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Simple admin credentials (in production, use proper authentication)
    if (credentials.username === 'admin' && credentials.password === 'denine2024') {
      localStorage.setItem('denine-admin', 'authenticated');
      onLogin(true);
    } else {
      setError('Invalid credentials');
    }
    setLoading(false);
  };

  return (
    <div className="section-spacing">
      <div className="container-artworld">
        <div style={{maxWidth: '400px', margin: '0 auto'}}>
          <div className="card-artworld">
            <div style={{padding: 'var(--spacing-xl)'}}>
              <h1 className="section-title text-center mb-lg">Admin Login</h1>
              
              <form onSubmit={handleSubmit}>
                <div className="mb-lg">
                  <label className="nav-link mb-sm" style={{display: 'block'}}>Username</label>
                  <input
                    type="text"
                    value={credentials.username}
                    onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                    style={{
                      width: '100%',
                      padding: 'var(--spacing-sm)',
                      border: '1px solid var(--color-gray-300)',
                      borderRadius: '4px',
                      fontFamily: 'var(--font-sans)',
                      fontSize: '1rem'
                    }}
                    placeholder="Enter username"
                    required
                  />
                </div>
                
                <div className="mb-lg">
                  <label className="nav-link mb-sm" style={{display: 'block'}}>Password</label>
                  <input
                    type="password"
                    value={credentials.password}
                    onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                    style={{
                      width: '100%',
                      padding: 'var(--spacing-sm)',
                      border: '1px solid var(--color-gray-300)',
                      borderRadius: '4px',
                      fontFamily: 'var(--font-sans)',
                      fontSize: '1rem'
                    }}
                    placeholder="Enter password"
                    required
                  />
                </div>
                
                {error && (
                  <div className="mb-lg" style={{color: '#dc2626', textAlign: 'center'}}>
                    <p className="caption-text">{error}</p>
                  </div>
                )}
                
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                  style={{width: '100%'}}
                >
                  {loading ? 'Signing In...' : 'Sign In'}
                </button>
              </form>
              
              <div className="mt-lg text-center">
                <p className="caption-text">Demo credentials: admin / denine2024</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
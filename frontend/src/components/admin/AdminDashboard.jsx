import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../../styles/artworld.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = ({ onLogout }) => {
  const [prints, setPrints] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('prints');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [printsRes] = await Promise.all([
        axios.get(`${API}/admin/prints`)
        // Add orders endpoint when ready
      ]);
      setPrints(printsRes.data.prints || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('denine-admin');
    onLogout(false);
  };

  if (loading) {
    return (
      <div className="section-spacing">
        <div className="container-artworld text-center">
          <h1 className="section-title">Loading Dashboard...</h1>
        </div>
      </div>
    );
  }

  return (
    <div className="section-spacing">
      <div className="container-artworld">
        {/* Header */}
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-xl)'}}>
          <h1 className="hero-title">Admin Dashboard</h1>
          <button onClick={handleLogout} className="btn-secondary">
            Logout
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="mb-xl">
          <div style={{display: 'flex', gap: 'var(--spacing-md)', borderBottom: '1px solid var(--color-gray-300)'}}>
            {[
              { key: 'prints', label: 'Print Management' },
              { key: 'pages', label: 'Page Content' },
              { key: 'orders', label: 'Orders' },
              { key: 'analytics', label: 'Analytics' }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`nav-link ${activeTab === tab.key ? 'text-black' : ''}`}
                style={{
                  background: 'none',
                  border: 'none',
                  padding: 'var(--spacing-md) 0',
                  borderBottom: activeTab === tab.key ? '2px solid var(--color-primary)' : 'none',
                  cursor: 'pointer'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'prints' && (
          <PrintManagement prints={prints} onRefresh={fetchData} />
        )}
        
        {activeTab === 'orders' && (
          <OrderManagement orders={orders} />
        )}
        
        {activeTab === 'analytics' && (
          <Analytics prints={prints} orders={orders} />
        )}

        {activeTab === 'pages' && (
          <PageManagement />
        )}
      </div>
    </div>
  );
};

// Print Management Component
const PrintManagement = ({ prints, onRefresh }) => {
  const [editingPrint, setEditingPrint] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);

  return (
    <div>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-xl)'}}>
        <h2 className="section-title">Print Collections</h2>
        <button 
          onClick={() => setShowAddForm(true)}
          className="btn-primary"
        >
          Add New Collection
        </button>
      </div>

      {/* Prints Grid */}
      <div className="artist-grid">
        {prints.map((print) => (
          <PrintCard 
            key={print.theme_id} 
            print={print} 
            onEdit={() => setEditingPrint(print)}
            onRefresh={onRefresh}
          />
        ))}
      </div>

      {/* Edit Modal */}
      {editingPrint && (
        <EditPrintModal 
          print={editingPrint} 
          onClose={() => setEditingPrint(null)}
          onSave={onRefresh}
        />
      )}
      
      {/* Add Form Modal */}
      {showAddForm && (
        <AddPrintModal 
          onClose={() => setShowAddForm(false)}
          onSave={onRefresh}
        />
      )}
    </div>
  );
};

// Individual Print Card
const PrintCard = ({ print, onEdit, onRefresh }) => {
  const featuredVariant = print.variants.find(v => v.featured);
  
  return (
    <div className="card-artworld">
      <img 
        src={featuredVariant?.image_url} 
        alt={print.theme}
        className="image-grid"
        style={{height: '200px'}}
      />
      <div style={{padding: 'var(--spacing-md)'}}>
        <h3 className="artist-name mb-xs">{print.theme}</h3>
        <p className="caption-text mb-sm" style={{height: '60px', overflow: 'hidden'}}>
          {print.description}
        </p>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <span className="body-text" style={{fontWeight: '500'}}>NOK {(print.base_price / 100).toFixed(0)}</span>
          <div style={{display: 'flex', gap: 'var(--spacing-xs)'}}>
            <button onClick={onEdit} className="btn-secondary" style={{padding: '0.5rem 1rem', fontSize: '0.75rem'}}>
              Edit
            </button>
          </div>
        </div>
        <div className="mt-sm">
          <span className="type-indicator">{print.variants.length} variants</span>
        </div>
      </div>
    </div>
  );
};

// Edit Print Modal
const EditPrintModal = ({ print, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    theme: print.theme,
    description: print.description,
    base_price: print.base_price
  });
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      await axios.put(`${API}/admin/prints/${print.theme_id}`, formData);
      onSave();
      onClose();
    } catch (error) {
      console.error('Error updating print:', error);
      alert('Failed to update print. Please try again.');
    }
    setSaving(false);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div className="card-artworld" style={{maxWidth: '600px', width: '90%', maxHeight: '90vh', overflow: 'auto'}}>
        <div style={{padding: 'var(--spacing-xl)'}}>
          <h2 className="artist-name mb-lg">Edit: {print.theme}</h2>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Theme Name</label>
            <input
              type="text"
              value={formData.theme}
              onChange={(e) => setFormData({...formData, theme: e.target.value})}
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)'
              }}
            />
          </div>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows="4"
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)',
                resize: 'vertical'
              }}
            />
          </div>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Price (NOK)</label>
            <input
              type="number"
              value={formData.base_price / 100}
              onChange={(e) => setFormData({...formData, base_price: parseInt(e.target.value * 100) || 0})}
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)'
              }}
            />
          </div>
          
          <div style={{display: 'flex', gap: 'var(--spacing-md)', justifyContent: 'flex-end'}}>
            <button onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button 
              onClick={handleSave} 
              className="btn-primary"
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Add Print Modal
const AddPrintModal = ({ onClose, onSave }) => {
  const [formData, setFormData] = useState({
    theme_id: '',
    theme: '',
    description: '',
    base_price: 19900
  });
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    if (!formData.theme_id || !formData.theme) {
      alert('Please fill in all required fields');
      return;
    }
    
    setSaving(true);
    try {
      await axios.post(`${API}/admin/prints`, formData);
      onSave();
      onClose();
    } catch (error) {
      console.error('Error creating print:', error);
      alert('Failed to create print. Please try again.');
    }
    setSaving(false);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div className="card-artworld" style={{maxWidth: '600px', width: '90%'}}>
        <div style={{padding: 'var(--spacing-xl)'}}>
          <h2 className="artist-name mb-lg">Add New Collection</h2>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Theme ID*</label>
            <input
              type="text"
              value={formData.theme_id}
              onChange={(e) => setFormData({...formData, theme_id: e.target.value})}
              placeholder="e.g., ocean-dreams-06"
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)'
              }}
            />
          </div>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Theme Name*</label>
            <input
              type="text"
              value={formData.theme}
              onChange={(e) => setFormData({...formData, theme: e.target.value})}
              placeholder="e.g., Ocean Dreams"
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)'
              }}
            />
          </div>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows="4"
              placeholder="Describe this print collection..."
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)',
                resize: 'vertical'
              }}
            />
          </div>
          
          <div className="mb-lg">
            <label className="nav-link mb-sm" style={{display: 'block'}}>Price (NOK)</label>
            <input
              type="number"
              value={formData.base_price / 100}
              onChange={(e) => setFormData({...formData, base_price: parseInt(e.target.value * 100) || 0})}
              style={{
                width: '100%',
                padding: 'var(--spacing-sm)',
                border: '1px solid var(--color-gray-300)',
                borderRadius: '4px',
                fontFamily: 'var(--font-sans)'
              }}
            />
          </div>
          
          <div style={{display: 'flex', gap: 'var(--spacing-md)', justifyContent: 'flex-end'}}>
            <button onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button 
              onClick={handleSave} 
              className="btn-primary"
              disabled={saving}
            >
              {saving ? 'Creating...' : 'Create Collection'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Order Management Component
const OrderManagement = ({ orders }) => {
  return (
    <div>
      <h2 className="section-title mb-xl">Order Management</h2>
      <div className="card-artworld">
        <div style={{padding: 'var(--spacing-xl)', textAlign: 'center'}}>
          <p className="body-text">Order management system will be available here.</p>
          <p className="caption-text mt-md">Currently showing recent orders and payment status.</p>
        </div>
      </div>
    </div>
  );
};

// Analytics Component
const Analytics = ({ prints, orders }) => {
  const totalCollections = prints.length;
  const totalVariants = prints.reduce((sum, print) => sum + print.variants.length, 0);
  
  return (
    <div>
      <h2 className="section-title mb-xl">Analytics Overview</h2>
      
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--spacing-lg)', marginBottom: 'var(--spacing-xl)'}}>
        <div className="card-artworld">
          <div style={{padding: 'var(--spacing-lg)', textAlign: 'center'}}>
            <div className="hero-title" style={{fontSize: '3rem', marginBottom: 'var(--spacing-sm)'}}>{totalCollections}</div>
            <div className="nav-link">Print Collections</div>
          </div>
        </div>
        
        <div className="card-artworld">
          <div style={{padding: 'var(--spacing-lg)', textAlign: 'center'}}>
            <div className="hero-title" style={{fontSize: '3rem', marginBottom: 'var(--spacing-sm)'}}>{totalVariants}</div>
            <div className="nav-link">Total Variants</div>
          </div>
        </div>
        
        <div className="card-artworld">
          <div style={{padding: 'var(--spacing-lg)', textAlign: 'center'}}>
            <div className="hero-title" style={{fontSize: '3rem', marginBottom: 'var(--spacing-sm)'}}>{orders.length}</div>
            <div className="nav-link">Total Orders</div>
          </div>
        </div>
      </div>
      
      <div className="card-artworld">
        <div style={{padding: 'var(--spacing-xl)'}}>
          <h3 className="artist-name mb-lg">Collection Performance</h3>
          <div style={{display: 'grid', gridTemplateColumns: '1fr', gap: 'var(--spacing-md)'}}>
            {prints.map(print => (
              <div key={print.theme_id} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: 'var(--spacing-sm)', borderBottom: '1px solid var(--color-gray-200)'}}>
                <span className="body-text">{print.theme}</span>
                <span className="caption-text">NOK {(print.base_price / 100).toFixed(0)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
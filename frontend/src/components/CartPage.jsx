import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/artworld.css';

export const CartPage = () => {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    const items = JSON.parse(localStorage.getItem('denine-cart') || '[]');
    setCartItems(items);
  }, []);

  const removeItem = (itemId) => {
    const updatedItems = cartItems.filter(item => item.id !== itemId);
    setCartItems(updatedItems);
    localStorage.setItem('denine-cart', JSON.stringify(updatedItems));
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    const updatedItems = cartItems.map(item => 
      item.id === itemId 
        ? { ...item, quantity: newQuantity, price: (item.price / item.quantity) * newQuantity }
        : item
    );
    setCartItems(updatedItems);
    localStorage.setItem('denine-cart', JSON.stringify(updatedItems));
  };

  const clearCart = () => {
    setCartItems([]);
    localStorage.removeItem('denine-cart');
  };

  const subtotal = cartItems.reduce((sum, item) => sum + item.price, 0);
  const shipping = subtotal > 0 ? 0 : 0; // Free shipping
  const total = subtotal + shipping;

  const proceedToCheckout = () => {
    alert(`Checkout functionality coming soon! Total: $${total}`);
  };

  if (cartItems.length === 0) {
    return (
      <div className="section-spacing">
        <div className="container-artworld text-center">
          <h1 className="section-title mb-md">Your Cart</h1>
          <p className="body-text mb-lg">Your cart is currently empty</p>
          <Link to="/gallery" className="btn-primary">
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="section-spacing">
      <div className="container-artworld">
        <h1 className="section-title mb-lg text-center">Your Cart</h1>

        <div style={{display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 'var(--spacing-3xl)'}}>
          {/* Cart Items */}
          <div>
            {cartItems.map((item, index) => (
              <div key={item.id} className={`card-artworld mb-lg fade-in-up stagger-${(index % 3) + 1}`}>
                <div style={{display: 'grid', gridTemplateColumns: 'auto 1fr auto', gap: 'var(--spacing-lg)', padding: 'var(--spacing-lg)'}}>
                  {/* Image */}
                  <div>
                    <img 
                      src={item.variants[0].image} 
                      alt={item.theme}
                      style={{width: '120px', height: '120px', objectFit: 'cover'}}
                    />
                  </div>

                  {/* Details */}
                  <div>
                    <h3 className="artist-name mb-xs">{item.theme}</h3>
                    <p className="caption-text mb-sm">{item.variantType} ({item.variants.length} prints)</p>
                    <div className="type-indicator mb-md">
                      {item.variants.map(v => v.name.split(' ').pop()).join(', ')}
                    </div>
                    
                    {/* Quantity Controls */}
                    <div style={{display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)'}}>
                      <span className="caption-text">Qty:</span>
                      <button 
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        style={{
                          padding: '0.25rem 0.5rem',
                          border: '1px solid #d1d5db',
                          background: 'white',
                          cursor: 'pointer'
                        }}
                      >
                        -
                      </button>
                      <span className="body-text" style={{minWidth: '2rem', textAlign: 'center'}}>
                        {item.quantity}
                      </span>
                      <button 
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        style={{
                          padding: '0.25rem 0.5rem',
                          border: '1px solid #d1d5db',
                          background: 'white',
                          cursor: 'pointer'
                        }}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  {/* Price & Remove */}
                  <div style={{textAlign: 'right'}}>
                    <div className="artist-name mb-md">${item.price}</div>
                    <button 
                      onClick={() => removeItem(item.id)}
                      className="nav-link"
                      style={{background: 'none', border: 'none', cursor: 'pointer', color: '#dc2626'}}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))}

            <div className="text-center">
              <button 
                onClick={clearCart}
                className="btn-secondary"
                style={{marginRight: 'var(--spacing-md)'}}
              >
                Clear Cart
              </button>
              <Link to="/gallery" className="btn-secondary">
                Continue Shopping
              </Link>
            </div>
          </div>

          {/* Order Summary */}
          <div>
            <div className="card-artworld" style={{position: 'sticky', top: '100px'}}>
              <div style={{padding: 'var(--spacing-lg)'}}>
                <h3 className="artist-name mb-lg text-center">Order Summary</h3>
                
                <div style={{marginBottom: 'var(--spacing-md)'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)'}}>
                    <span className="caption-text">Subtotal:</span>
                    <span className="body-text">${subtotal}</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)'}}>
                    <span className="caption-text">Shipping:</span>
                    <span className="body-text">{shipping === 0 ? 'Free' : `$${shipping}`}</span>
                  </div>
                  <div 
                    style={{
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      borderTop: '1px solid #e5e7eb', 
                      paddingTop: 'var(--spacing-sm)',
                      marginTop: 'var(--spacing-md)'
                    }}
                  >
                    <span className="body-text" style={{fontWeight: '600'}}>Total:</span>
                    <span className="artist-name">${total}</span>
                  </div>
                </div>

                <button 
                  onClick={proceedToCheckout}
                  className="btn-primary"
                  style={{width: '100%', marginBottom: 'var(--spacing-md)'}}
                >
                  Proceed to Checkout
                </button>

                <div className="caption-text text-center">
                  <p style={{marginBottom: 'var(--spacing-xs)'}}>🔒 Secure Checkout</p>
                  <p>Free worldwide shipping</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
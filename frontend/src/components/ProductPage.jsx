import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { prints, shippingInfo } from '../data/mock';
import '../styles/artworld.css';

export const ProductPage = () => {
  const { id } = useParams();
  const print = prints.find(p => p.id === id);
  const [selectedVariants, setSelectedVariants] = useState([print?.variants[0]]);
  const [quantity, setQuantity] = useState(1);

  if (!print) {
    return (
      <div className="section-spacing">
        <div className="container-artworld text-center">
          <h1 className="section-title mb-md">Print Not Found</h1>
          <Link to="/gallery" className="btn-primary">
            Return to Gallery
          </Link>
        </div>
      </div>
    );
  }

  const handleVariantToggle = (variant) => {
    setSelectedVariants(prev => {
      const isSelected = prev.some(v => v.id === variant.id);
      if (isSelected) {
        return prev.filter(v => v.id !== variant.id);
      } else if (prev.length < 3) {
        return [...prev, variant];
      } else {
        return prev;
      }
    });
  };

  const totalPrice = selectedVariants.length * print.price * quantity;
  const variantText = selectedVariants.length === 1 ? 'Single Print' : 
                     selectedVariants.length === 2 ? 'Pair' : 'Triptych';

  const addToCart = () => {
    const cartItem = {
      id: `${print.id}-${selectedVariants.map(v => v.id).join('-')}`,
      printId: print.id,
      theme: print.theme,
      variants: selectedVariants,
      quantity: quantity,
      price: totalPrice,
      variantType: variantText
    };
    
    // Store in localStorage (mock cart functionality)
    const existingCart = JSON.parse(localStorage.getItem('denine-cart') || '[]');
    existingCart.push(cartItem);
    localStorage.setItem('denine-cart', JSON.stringify(existingCart));
    
    alert(`Added ${variantText} (${selectedVariants.length} prints) to cart!`);
  };

  return (
    <div className="section-spacing">
      <div className="container-artworld">
        {/* Breadcrumb */}
        <div className="mb-lg">
          <Link to="/gallery" className="nav-link">← Gallery</Link>
        </div>

        <div className="product-layout">
          {/* Images */}
          <div className="product-images">
            {print.variants.map((variant, index) => (
              <div key={variant.id} className={`fade-in-up stagger-${index + 1}`}>
                <img 
                  src={variant.image} 
                  alt={variant.name}
                  className="image-product"
                />
                <div className="text-center mt-sm">
                  <h4 className="type-indicator">{variant.name}</h4>
                </div>
              </div>
            ))}
          </div>

          {/* Product Info */}
          <div className="product-info">
            <h1 className="section-title mb-sm">{print.theme}</h1>
            <p className="body-text mb-lg">{print.description}</p>

            {/* Variant Selection */}
            <div className="mb-lg">
              <h3 className="artist-name mb-md">Select Your Print(s)</h3>
              
              {/* Individual Variant Selection First */}
              <div className="mb-lg">
                <h4 className="nav-link mb-md">Choose Specific Variant(s):</h4>
                <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem'}}>
                  {print.variants.map((variant) => (
                    <div 
                      key={variant.id}
                      className={`variant-option ${
                        selectedVariants.some(v => v.id === variant.id) ? 'selected' : ''
                      }`}
                      onClick={() => handleVariantToggle(variant)}
                      style={{padding: '0.75rem', cursor: 'pointer'}}
                    >
                      <img 
                        src={variant.image} 
                        alt={variant.name}
                        style={{width: '100%', height: '80px', objectFit: 'cover', marginBottom: '0.5rem'}}
                      />
                      <div className="type-indicator" style={{fontSize: '0.75rem', marginBottom: '0.25rem'}}>
                        {variant.name}
                      </div>
                      <div className="variant-price" style={{fontSize: '0.7rem'}}>
                        ${print.price}
                      </div>
                    </div>
                  ))}
                </div>
                <p className="caption-text mt-sm">
                  Select {selectedVariants.length === 0 ? '1-3' : selectedVariants.length < 3 ? `${selectedVariants.length} more or finish selection` : 'up to 3'} variant(s). 
                  Click variants above to select specific prints.
                </p>
              </div>

              {/* Configuration Summary */}
              <div className="product-variants">
                <div 
                  className={`variant-option ${
                    selectedVariants.length === 1 ? 'selected' : ''
                  }`}
                  onClick={() => selectedVariants.length === 0 ? setSelectedVariants([print.variants[0]]) : null}
                  style={{cursor: selectedVariants.length === 0 ? 'pointer' : 'default', opacity: selectedVariants.length === 1 ? 1 : 0.6}}
                >
                  <div className="variant-number">1</div>
                  <div className="variant-label">Single Print</div>
                  <div className="variant-price">${print.price}</div>
                </div>
                
                <div 
                  className={`variant-option ${
                    selectedVariants.length === 2 ? 'selected' : ''
                  }`}
                  style={{cursor: 'default', opacity: selectedVariants.length === 2 ? 1 : 0.6}}
                >
                  <div className="variant-number">2</div>
                  <div className="variant-label">Pair</div>
                  <div className="variant-price">${print.price * 2}</div>
                </div>
                
                <div 
                  className={`variant-option ${
                    selectedVariants.length === 3 ? 'selected' : ''
                  }`}
                  style={{cursor: 'default', opacity: selectedVariants.length === 3 ? 1 : 0.6}}
                >
                  <div className="variant-number">3</div>
                  <div className="variant-label">Triptych</div>
                  <div className="variant-price">${print.price * 3}</div>
                </div>
              </div>
            </div>

            {/* Quantity */}
            <div className="mb-lg">
              <label className="nav-link mb-sm" style={{display: 'block'}}>Quantity</label>
              <select 
                value={quantity} 
                onChange={(e) => setQuantity(Number(e.target.value))}
                style={{
                  padding: '0.5rem', 
                  border: '1px solid #d1d5db', 
                  backgroundColor: 'white',
                  fontFamily: 'var(--font-sans)',
                  fontSize: '1rem'
                }}
              >
                {[1,2,3,4,5].map(num => (
                  <option key={num} value={num}>{num}</option>
                ))}
              </select>
            </div>

            {/* Price */}
            <div className="mb-lg">
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <span className="body-text">{variantText} × {quantity}</span>
                <span className="section-title">${totalPrice}</span>
              </div>
            </div>

            {/* Add to Cart */}
            <button 
              className="btn-primary" 
              onClick={addToCart}
              style={{width: '100%', marginBottom: 'var(--spacing-lg)'}}
            >
              Add to Cart
            </button>

            {/* Product Details */}
            <div className="mt-xl" style={{borderTop: '1px solid #e5e7eb', paddingTop: 'var(--spacing-lg)'}}>
              <h4 className="nav-link mb-md">Product Details</h4>
              <div className="caption-text" style={{lineHeight: '1.8'}}>
                <p><strong>Size:</strong> {shippingInfo.size}</p>
                <p><strong>Material:</strong> {shippingInfo.paper}</p>
                <p><strong>Delivery:</strong> {shippingInfo.delivery}</p>
                <p><strong>Shipping:</strong> {shippingInfo.shipping}</p>
                <p><strong>Packaging:</strong> {shippingInfo.packaging}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
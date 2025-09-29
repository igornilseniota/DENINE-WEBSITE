import React from 'react';
import { Link } from 'react-router-dom';
import { prints } from '../data/mock';
import '../styles/artworld.css';

export const GalleryPage = () => {
  return (
    <div className="section-spacing">
      <div className="container-artworld">
        {/* Header */}
        <div className="text-center mb-xl">
          <h1 className="hero-title mb-md">Gallery</h1>
          <p className="body-text">
            Explore our complete collection of fine art prints. Each theme offers three complementary variants, perfect alone or as curated sets.
          </p>
        </div>

        {/* Gallery Grid */}
        <div className="artist-grid">
          {prints.map((print, index) => {
            const featuredVariant = print.variants.find(v => v.featured);
            return (
              <div key={print.id} className={`card-artworld fade-in-up stagger-${(index % 3) + 1}`}>
                <Link to={`/print/${print.id}`}>
                  <img 
                    src={featuredVariant.image} 
                    alt={print.theme}
                    className="image-grid"
                  />
                </Link>
                <div className="card-content">
                  <h3 className="artist-name mb-xs">{print.theme}</h3>
                  <p className="caption-text mb-md">{print.description}</p>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span className="body-text" style={{fontWeight: '500'}}>${print.price}</span>
                    <Link to={`/print/${print.id}`} className="btn-secondary">
                      View Collection
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Info Section */}
        <div className="section-spacing-large">
          <div className="text-center">
            <h2 className="section-title mb-md">About Our Prints</h2>
            <div className="body-text" style={{maxWidth: '600px', margin: '0 auto'}}>
              <p className="mb-md">
                Each print in our collection is carefully produced on premium 50x70cm fine art paper, 
                ensuring exceptional quality and longevity.
              </p>
              <p>
                Our unique approach offers three variants of each theme, allowing you to create 
                personalized arrangements that perfectly suit your space.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GalleryPage;
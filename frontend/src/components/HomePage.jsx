import React from 'react';
import { Link } from 'react-router-dom';
import { prints, testimonials, shippingInfo } from '../data/mock';
import '../styles/artworld.css';

export const HomePage = () => {
  // Get featured print for hero
  const featuredPrint = prints[0];
  const featuredVariant = featuredPrint.variants.find(v => v.featured);

  return (
    <div>
      {/* Hero Section */}
      <section className="hero-section">
        <img 
          src={featuredVariant.image} 
          alt={featuredPrint.theme}
          className="hero-background"
        />
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1 className="hero-title fade-in-up">Fine Art Prints</h1>
          <p className="body-text hero-subtitle fade-in-up stagger-1">
            Premium 70x50cm prints on fine art paper. Beautiful alone, stunning as pairs or triptychs.
          </p>
          <Link to="/gallery" className="btn-primary fade-in-up stagger-2">
            Explore Gallery
          </Link>
        </div>
      </section>

      {/* Featured Collection */}
      <section className="section-spacing">
        <div className="container-artworld">
          <div className="text-center mb-xl">
            <h2 className="section-title mb-md">Featured Collections</h2>
            <p className="body-text">
              Discover our curated selection of abstract landscape prints, each theme available in three complementary variants.
            </p>
          </div>
          
          <div className="artist-grid">
            {prints.slice(0, 3).map((print, index) => {
              const featuredVariant = print.variants.find(v => v.featured);
              return (
                <div key={print.id} className={`card-artworld fade-in-up stagger-${index + 1}`}>
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
                    <div className="flex justify-between items-center">
                      <span className="body-text font-medium">${print.price}</span>
                      <Link to={`/print/${print.id}`} className="btn-secondary">
                        View Collection
                      </Link>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          
          <div className="text-center mt-xl">
            <Link to="/gallery" className="btn-primary">
              View All Collections
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="section-spacing gallery-section">
        <div className="container-artworld">
          <div className="text-center mb-xl">
            <h2 className="section-title mb-md">How It Works</h2>
            <p className="body-text">
              Each theme offers three variants that work beautifully alone or together.
            </p>
          </div>
          
          <div className="artist-grid">
            <div className="text-center">
              <div className="variant-number mb-md">1</div>
              <h3 className="artist-name mb-sm">Single Print</h3>
              <p className="caption-text">
                Perfect as a focal point. Each print makes a powerful statement on its own.
              </p>
            </div>
            
            <div className="text-center">
              <div className="variant-number mb-md">2</div>
              <h3 className="artist-name mb-sm">Pair</h3>
              <p className="caption-text">
                Two complementary variants create visual dialogue and balance.
              </p>
            </div>
            
            <div className="text-center">
              <div className="variant-number mb-md">3</div>
              <h3 className="artist-name mb-sm">Triptych</h3>
              <p className="caption-text">
                Three variants form a cohesive narrative across your wall.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Quality Promise */}
      <section className="section-spacing">
        <div className="container-artworld">
          <div className="text-center mb-xl">
            <h2 className="section-title mb-md">Premium Quality</h2>
            <p className="body-text">
              Every print is produced to museum standards using premium materials.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <h4 className="nav-link mb-sm">{shippingInfo.size}</h4>
              <p className="caption-text">Standard size for perfect impact</p>
            </div>
            
            <div className="text-center">
              <h4 className="nav-link mb-sm">{shippingInfo.paper}</h4>
              <p className="caption-text">Archival quality materials</p>
            </div>
            
            <div className="text-center">
              <h4 className="nav-link mb-sm">{shippingInfo.shipping}</h4>
              <p className="caption-text">Delivered worldwide</p>
            </div>
            
            <div className="text-center">
              <h4 className="nav-link mb-sm">{shippingInfo.packaging}</h4>
              <p className="caption-text">Protected during transit</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="section-spacing gallery-section">
        <div className="container-artworld">
          <div className="text-center mb-xl">
            <h2 className="section-title mb-md">Customer Stories</h2>
          </div>
          
          <div className="artist-grid">
            {testimonials.map((testimonial, index) => (
              <div key={index} className={`text-center fade-in-up stagger-${index + 1}`}>
                <p className="body-text mb-md italic">"{testimonial.text}"</p>
                <div>
                  <h4 className="nav-link mb-xs">{testimonial.name}</h4>
                  <p className="caption-text">{testimonial.location}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
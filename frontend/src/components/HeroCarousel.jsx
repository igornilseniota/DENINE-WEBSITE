import React, { useState, useEffect } from 'react';
import { prints } from '../data/mock';
import '../styles/artworld.css';

export const HeroCarousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  // Get featured images from all prints for the carousel
  const heroImages = prints.map(print => {
    const featuredVariant = print.variants.find(v => v.featured);
    return {
      image: featuredVariant.image,
      theme: print.theme,
      description: print.description
    };
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroImages.length);
    }, 4000); // Change slide every 4 seconds

    return () => clearInterval(interval);
  }, [heroImages.length]);

  return (
    <div className="hero-carousel">
      {heroImages.map((item, index) => (
        <div 
          key={index}
          className={`hero-slide ${index === currentSlide ? 'active' : ''}`}
        >
          <img 
            src={item.image} 
            alt={item.theme}
            className="hero-background"
          />
        </div>
      ))}
      <div className="hero-overlay"></div>
    </div>
  );
};

export default HeroCarousel;
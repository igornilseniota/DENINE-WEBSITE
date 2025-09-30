import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/artworld.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const HeroCarousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [heroImages, setHeroImages] = useState([]);

  useEffect(() => {
    fetchPrints();
  }, []);

  useEffect(() => {
    if (heroImages.length > 0) {
      const interval = setInterval(() => {
        setCurrentSlide((prev) => (prev + 1) % heroImages.length);
      }, 4000); // Change slide every 4 seconds

      return () => clearInterval(interval);
    }
  }, [heroImages.length]);

  const fetchPrints = async () => {
    try {
      const response = await axios.get(`${API}/prints`);
      const prints = response.data.prints || [];
      
      // Get featured images from all prints for the carousel
      const images = prints.map(print => {
        const featuredVariant = print.variants.find(v => v.featured);
        return {
          image: featuredVariant?.image_url,
          theme: print.theme,
          description: print.description
        };
      }).filter(item => item.image); // Filter out items without images
      
      setHeroImages(images);
    } catch (err) {
      console.error('Error fetching prints for carousel:', err);
      // Fallback to empty array
      setHeroImages([]);
    }
  };

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
      
      {/* Carousel Indicators */}
      <div className="carousel-indicators">
        {heroImages.map((_, index) => (
          <button
            key={index}
            className={`carousel-dot ${index === currentSlide ? 'active' : ''}`}
            onClick={() => setCurrentSlide(index)}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
};

export default HeroCarousel;
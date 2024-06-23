import React, { useState } from 'react';
import "./PhishingDetection.css";
import { checkUrl, checkImage } from '../services/api';

const PhishingDetection: React.FC = () => {
  const [url, setUrl] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [showWarning, setShowWarning] = useState(false);

  const handleUrlCheck = async () => {
    try {
      const isPhishing = await checkUrl(url);
      if (isPhishing) {
        setMessage('This URL may be a phishing site!');
        setShowWarning(true);
      } else {
        setMessage('This URL is safe.');
        setShowWarning(false);
      }
    } catch (error) {
      setMessage('Error checking URL.');
      setShowWarning(false);
    }
  };

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setImage(file);

      try {
        const isPhishingImage = await checkImage(file);
        if (isPhishingImage) {
          setMessage('This image may be related to a phishing site!');
          setShowWarning(true);
        } else {
          setMessage('This image is safe.');
          setShowWarning(false);
        }
      } catch (error) {
        setMessage('Error checking image.');
        setShowWarning(false);
      }
    }
  };

  return (
    <div className="phishing-tracker-page">
      <div className="phishing-content-overlay">
        <h2 className="phishing-page-title">Phishing Tracker</h2>
        <div className="url-checker">
          <input 
            type="text" 
            placeholder="Enter URL to check" 
            value={url} 
            onChange={(e) => setUrl(e.target.value)} 
          />
          <button onClick={handleUrlCheck}>Check URL</button>
        </div>
        <div className="image-checker">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleImageUpload} 
          />
          <button>Upload Image</button>
        </div>
        {message && (
          <div className={`message ${showWarning ? 'warning' : 'safe'}`}>
            {message}
          </div>
        )}
      </div>
      <video autoPlay loop muted className="phishing-background-video">
      <source src="/starwar_background.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    </div>
  );
};


export default PhishingDetection;

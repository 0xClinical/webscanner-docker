import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';
import { login } from '../services/api';

interface LoginProps {
  onLogin: (token: string) => void;
}
interface LoginResult{
  status: string,
  message: string
}
const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response:LoginResult = await login(email,password);
      if (response.status ==='succcess') {
        onLogin(response.message);
      }else{
        alert(response.message);
      }
      onLogin(response.message);
      
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="login-button">Login</button>
        </form>
      </div>
      <video autoPlay loop muted className="background-video">
      <source src="/robot_background.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    </div>
  );
};

export default Login;

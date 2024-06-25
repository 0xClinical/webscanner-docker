import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';
import { login, register } from '../services/api';

interface LoginProps {
  onLogin: (token: string, user: any) => void;
}
interface LoginResult {
  status: string;
  message: string;
  token?: string;
  user?: any;
}
const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showRegister, setShowRegister] = useState(false);
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerError, setRegisterError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response: LoginResult = await login(email, password);
      if (response.status === 'success') {
        onLogin(response.token!, response.user!);
      } else {
        setError(response.message);
      }
      alert('login success!');
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await register(registerEmail, registerPassword);
      if (response.status === 'success') {
        setShowRegister(false);
        alert('Registration successful. Please log in.');
      } else {
        setRegisterError(response.message);
      }
    } catch (err) {
      setRegisterError('Registration failed');
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
          <div className="button-group">
            <button type="submit" className="login-button">Login</button>
            <button onClick={() => setShowRegister(true)} className="register-button">Register</button>
          </div>
        </form>
      </div>
      <video autoPlay loop muted className="background-video">
        <source src="/robot_background.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {showRegister && (
        <div className="register-modal">
          <div className="register-box">
            <h2 className="register-title">Register</h2>
            <form onSubmit={handleRegister}>
              <div className="input-group">
                <label>Email</label>
                <input
                  type="email"
                  value={registerEmail}
                  onChange={(e) => setRegisterEmail(e.target.value)}
                  required
                />
              </div>
              <div className="input-group">
                <label>Password</label>
                <input
                  type="password"
                  value={registerPassword}
                  onChange={(e) => setRegisterPassword(e.target.value)}
                  required
                />
              </div>
              {registerError && <p className="error-message">{registerError}</p>}
              <div className="button-group">
                <button type="submit" className="register-button">Register</button>
                <button onClick={() => setShowRegister(false)} className="close-button">Close</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Login;

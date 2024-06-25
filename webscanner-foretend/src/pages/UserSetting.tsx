import React, { useState } from 'react';
import './UserSetting.css';
import { changePwd } from '../services/api';

interface UserSettingsProps {
  user: {
    id: number;
    email: string;
    role: string;
    created_at: string;
  };
}

const UserSettings: React.FC<UserSettingsProps> = ({ user }) => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      setMessage('');
      return;
    }
    try {
      const response = await changePwd(user.id, user.email, newPassword);
      if (response.status === 'success') {
        setMessage('Password updated successfully');
        setError('');
      } else {
        setError(response.message);
        setMessage('');
      }
    } catch (err) {
      setError('Failed to update password');
      setMessage('');
    }
  };

  return (
    <div className="user-settings-wrapper">
      <div className="user-settings-container">
        <h2>User Settings</h2>
        <div className="user-info">
          <p><strong>ID:</strong> {user.id}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Role:</strong> {user.role}</p>
          <p><strong>Created At:</strong> {user.created_at}</p>
        </div>
        <form onSubmit={handlePasswordChange} className="password-change-form">
          <h3>Change Password</h3>
          <div className="input-group">
            <label>New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          {message && <p className="success-message">{message}</p>}
          <button type="submit" className="change-password-button">Change Password</button>
        </form>
      </div>
      <video autoPlay loop muted className="background-video">
        <source src="/steampunk-background.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default UserSettings;

import React from 'react';
import './UserSetting.css';

interface UserSettingsProps {
  user: {
    id: number;
    email: string;
    role: string;
    created_at: string;
  };
}

const UserSettings: React.FC<UserSettingsProps> = ({ user }) => {
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
      </div>
      <video autoPlay loop muted className="background-video">
        <source src="/steampunk-background.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default UserSettings;

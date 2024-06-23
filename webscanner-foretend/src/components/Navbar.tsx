import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar: React.FC = () => {
    return (
        <nav className="navbar">
        <div className="nav-links">
          <NavLink
            to="/vulnerability-scan"
            className={({ isActive }) => "nav-link" + (isActive ? " nav-link-active" : "")}
          >
            <i className="fas fa-bug"></i> Scan
          </NavLink>
          <NavLink
            to="/vulnerability-info"
            className={({ isActive }) => "nav-link" + (isActive ? " nav-link-active" : "")}
          >
            <i className="fas fa-info-circle"></i> Info
          </NavLink>
          <NavLink
            to="/dashboard"
            className={({ isActive }) => "nav-link" + (isActive ? " nav-link-active" : "")}
          >
            <i className="fas fa-tachometer-alt"></i> Dashboard
          </NavLink>
          <NavLink
            to="/phishing-detection"
            className={({ isActive }) => "nav-link" + (isActive ? " nav-link-active" : "")}
          >
            <i className="fas fa-fish"></i> Phishing
          </NavLink>
        </div>
        <NavLink
          to="/user-settings"
          className={({ isActive }) => "user-settings" + (isActive ? " nav-link-active" : "")}
        >
          <i className="fas fa-user-cog"></i> User Settings
        </NavLink>
      </nav>
      );
};

export default Navbar;

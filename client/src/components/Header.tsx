import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <h1>🏃‍♂️ Garmin Training Dashboard</h1>
        </div>
        <nav className="nav">
          <button className="nav-button">Dashboard</button>
          <button className="nav-button">Activities</button>
          <button className="nav-button">Health</button>
          <button className="nav-button">Settings</button>
        </nav>
      </div>
    </header>
  );
};

export default Header;


import React from 'react';
import { useGarminData } from '../context/GarminDataContext';
import ActivityChart from './ActivityChart';
import HealthMetrics from './HealthMetrics';
import ActivityList from './ActivityList';
import StatsOverview from './StatsOverview';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { isLoading, error, refreshData } = useGarminData();

  if (error) {
    return (
      <div className="error-container">
        <div className="error">
          <h3>⚠️ Error Loading Data</h3>
          <p>{error}</p>
          <button onClick={refreshData} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Your Training Overview</h2>
        <button 
          onClick={refreshData} 
          className="refresh-button"
          disabled={isLoading}
        >
          {isLoading ? '🔄 Refreshing...' : '🔄 Refresh Data'}
        </button>
      </div>

      <div className="dashboard-grid">
        <StatsOverview />
        <ActivityChart />
        <HealthMetrics />
        <ActivityList />
      </div>
    </div>
  );
};

export default Dashboard;


import React from 'react';
import { useGarminData } from '../context/GarminDataContext';
import './StatsOverview.css';

const StatsOverview: React.FC = () => {
  const { activities, healthData, isLoading } = useGarminData();

  // Calculate stats from activities and health data
  const totalActivities = activities.length;
  const totalDistance = activities.reduce((sum, activity) => sum + (activity.distance || 0), 0);
  const totalCalories = activities.reduce((sum, activity) => sum + (activity.calories || 0), 0);
  const avgHeartRate = healthData.length > 0 
    ? healthData.reduce((sum, data) => sum + (data.heartRate || 0), 0) / healthData.length 
    : 0;

  const stats = [
    {
      label: 'Total Activities',
      value: totalActivities,
      icon: '🏃‍♂️',
      color: '#3498db'
    },
    {
      label: 'Total Distance',
      value: `${(totalDistance / 1000).toFixed(1)} km`,
      icon: '📏',
      color: '#2ecc71'
    },
    {
      label: 'Total Calories',
      value: totalCalories.toLocaleString(),
      icon: '🔥',
      color: '#e74c3c'
    },
    {
      label: 'Avg Heart Rate',
      value: `${Math.round(avgHeartRate)} bpm`,
      icon: '❤️',
      color: '#9b59b6'
    }
  ];

  if (isLoading) {
    return (
      <div className="card stats-overview">
        <h3>📊 Quick Stats</h3>
        <div className="loading">Loading stats...</div>
      </div>
    );
  }

  return (
    <div className="card stats-overview">
      <h3>📊 Quick Stats</h3>
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-item">
            <div className="stat-icon" style={{ backgroundColor: stat.color }}>
              {stat.icon}
            </div>
            <div className="stat-content">
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StatsOverview;


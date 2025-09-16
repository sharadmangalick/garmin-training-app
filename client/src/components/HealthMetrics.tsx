import React from 'react';
import { useGarminData } from '../context/GarminDataContext';
import './HealthMetrics.css';

const HealthMetrics: React.FC = () => {
  const { healthData, isLoading } = useGarminData();

  // Process health data for display
  const processHealthData = () => {
    if (healthData.length === 0) {
      return {
        avgHeartRate: 0,
        maxHeartRate: 0,
        minHeartRate: 0,
        avgSteps: 0,
        avgSleep: 0,
        avgStress: 0
      };
    }

    const heartRates = healthData.map(data => data.heartRate || 0).filter(hr => hr > 0);
    const steps = healthData.map(data => data.steps || 0);
    const sleep = healthData.map(data => data.sleepMinutes || 0);
    const stress = healthData.map(data => data.stressLevel || 0);

    return {
      avgHeartRate: heartRates.length > 0 ? Math.round(heartRates.reduce((a, b) => a + b, 0) / heartRates.length) : 0,
      maxHeartRate: heartRates.length > 0 ? Math.max(...heartRates) : 0,
      minHeartRate: heartRates.length > 0 ? Math.min(...heartRates) : 0,
      avgSteps: Math.round(steps.reduce((a, b) => a + b, 0) / steps.length),
      avgSleep: Math.round(sleep.reduce((a, b) => a + b, 0) / sleep.length),
      avgStress: Math.round(stress.reduce((a, b) => a + b, 0) / stress.length)
    };
  };

  const health = processHealthData();

  const metrics = [
    {
      label: 'Avg Heart Rate',
      value: `${health.avgHeartRate} bpm`,
      icon: '❤️',
      color: '#e74c3c',
      range: health.avgHeartRate > 0 ? `${health.minHeartRate}-${health.maxHeartRate} bpm` : 'No data'
    },
    {
      label: 'Daily Steps',
      value: health.avgSteps.toLocaleString(),
      icon: '👣',
      color: '#2ecc71',
      range: 'Average per day'
    },
    {
      label: 'Sleep Duration',
      value: `${Math.floor(health.avgSleep / 60)}h ${health.avgSleep % 60}m`,
      icon: '😴',
      color: '#3498db',
      range: 'Average per night'
    },
    {
      label: 'Stress Level',
      value: health.avgStress > 0 ? `${health.avgStress}/100` : 'No data',
      icon: '🧘‍♂️',
      color: health.avgStress > 50 ? '#e67e22' : '#27ae60',
      range: 'Lower is better'
    }
  ];

  if (isLoading) {
    return (
      <div className="card health-metrics">
        <h3>💓 Health Metrics</h3>
        <div className="loading">Loading health data...</div>
      </div>
    );
  }

  return (
    <div className="card health-metrics">
      <h3>💓 Health Metrics</h3>
      <div className="metrics-grid">
        {metrics.map((metric, index) => (
          <div key={index} className="metric-item">
            <div className="metric-header">
              <div className="metric-icon" style={{ backgroundColor: metric.color }}>
                {metric.icon}
              </div>
              <div className="metric-content">
                <div className="metric-value">{metric.value}</div>
                <div className="metric-label">{metric.label}</div>
              </div>
            </div>
            <div className="metric-range">{metric.range}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HealthMetrics;


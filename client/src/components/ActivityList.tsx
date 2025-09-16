import React, { useState } from 'react';
import { useGarminData } from '../context/GarminDataContext';
import { format, parseISO } from 'date-fns';
import './ActivityList.css';

const ActivityList: React.FC = () => {
  const { activities, isLoading } = useGarminData();
  const [filter, setFilter] = useState('all');

  const getActivityIcon = (activityType: string) => {
    const type = activityType?.toLowerCase() || '';
    if (type.includes('running')) return '🏃‍♂️';
    if (type.includes('cycling') || type.includes('biking')) return '🚴‍♂️';
    if (type.includes('swimming')) return '🏊‍♂️';
    if (type.includes('walking')) return '🚶‍♂️';
    if (type.includes('hiking')) return '🥾';
    if (type.includes('strength') || type.includes('weight')) return '💪';
    return '🏃‍♂️';
  };

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  };

  const filteredActivities = activities.filter(activity => {
    if (filter === 'all') return true;
    const type = activity.activityType?.toLowerCase() || '';
    return type.includes(filter);
  });

  const activityTypes = ['all', 'running', 'cycling', 'swimming', 'walking', 'hiking', 'strength'];

  if (isLoading) {
    return (
      <div className="card activity-list">
        <h3>📋 Recent Activities</h3>
        <div className="loading">Loading activities...</div>
      </div>
    );
  }

  return (
    <div className="card activity-list">
      <div className="activity-list-header">
        <h3>📋 Recent Activities</h3>
        <div className="activity-filters">
          {activityTypes.map(type => (
            <button
              key={type}
              className={`filter-button ${filter === type ? 'active' : ''}`}
              onClick={() => setFilter(type)}
            >
              {type === 'all' ? 'All' : type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>
      
      <div className="activities-container">
        {filteredActivities.length === 0 ? (
          <div className="no-activities">
            <p>No activities found for the selected filter.</p>
            <p>Make sure your Garmin Connect account is connected and has recent activities.</p>
          </div>
        ) : (
          <div className="activities-list">
            {filteredActivities.slice(0, 10).map((activity, index) => (
              <div key={activity.activityId || index} className="activity-item">
                <div className="activity-icon">
                  {getActivityIcon(activity.activityType?.typeKey || '')}
                </div>
                <div className="activity-details">
                  <div className="activity-name">
                    {activity.activityName || `${activity.activityType?.typeKey || 'Activity'} - ${format(parseISO(activity.startTimeLocal || activity.startTime), 'MMM dd, yyyy')}`}
                  </div>
                  <div className="activity-meta">
                    <span className="activity-type">
                      {activity.activityType?.typeKey || 'Unknown'}
                    </span>
                    <span className="activity-date">
                      {format(parseISO(activity.startTimeLocal || activity.startTime), 'MMM dd, HH:mm')}
                    </span>
                  </div>
                </div>
                <div className="activity-stats">
                  {activity.distance && (
                    <div className="stat">
                      <span className="stat-value">{(activity.distance / 1000).toFixed(1)}</span>
                      <span className="stat-unit">km</span>
                    </div>
                  )}
                  {activity.elapsedDuration && (
                    <div className="stat">
                      <span className="stat-value">{formatDuration(activity.elapsedDuration)}</span>
                    </div>
                  )}
                  {activity.calories && (
                    <div className="stat">
                      <span className="stat-value">{activity.calories}</span>
                      <span className="stat-unit">cal</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ActivityList;


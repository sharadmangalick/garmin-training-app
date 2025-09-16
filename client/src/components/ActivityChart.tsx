import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useGarminData } from '../context/GarminDataContext';
import { format, subDays } from 'date-fns';
import './ActivityChart.css';

const ActivityChart: React.FC = () => {
  const { activities, isLoading } = useGarminData();

  // Process activities data for the chart
  const processChartData = () => {
    const last7Days = Array.from({ length: 7 }, (_, i) => {
      const date = subDays(new Date(), 6 - i);
      return {
        date: format(date, 'MMM dd'),
        fullDate: date,
        distance: 0,
        calories: 0,
        activities: 0
      };
    });

    activities.forEach(activity => {
      const activityDate = new Date(activity.startTimeLocal || activity.startTime);
      const dayIndex = last7Days.findIndex(day => 
        day.fullDate.toDateString() === activityDate.toDateString()
      );
      
      if (dayIndex !== -1) {
        last7Days[dayIndex].distance += (activity.distance || 0) / 1000; // Convert to km
        last7Days[dayIndex].calories += activity.calories || 0;
        last7Days[dayIndex].activities += 1;
      }
    });

    return last7Days.map(({ date, distance, calories, activities }) => ({
      date,
      distance: Math.round(distance * 10) / 10,
      calories,
      activities
    }));
  };

  const chartData = processChartData();

  if (isLoading) {
    return (
      <div className="card activity-chart">
        <h3>📈 Activity Trends</h3>
        <div className="loading">Loading chart data...</div>
      </div>
    );
  }

  return (
    <div className="card activity-chart">
      <h3>📈 Activity Trends (Last 7 Days)</h3>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e1e5e9" />
            <XAxis 
              dataKey="date" 
              stroke="#6c757d"
              fontSize={12}
            />
            <YAxis 
              stroke="#6c757d"
              fontSize={12}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e1e5e9',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="distance" 
              stroke="#3498db" 
              strokeWidth={3}
              dot={{ fill: '#3498db', strokeWidth: 2, r: 4 }}
              name="Distance (km)"
            />
            <Line 
              type="monotone" 
              dataKey="calories" 
              stroke="#e74c3c" 
              strokeWidth={3}
              dot={{ fill: '#e74c3c', strokeWidth: 2, r: 4 }}
              name="Calories"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="chart-legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#3498db' }}></div>
          <span>Distance (km)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#e74c3c' }}></div>
          <span>Calories</span>
        </div>
      </div>
    </div>
  );
};

export default ActivityChart;


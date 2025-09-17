import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import axios from 'axios';

// Types used by frontend components
export type ActivityType = {
  typeKey?: string;
};

export type Activity = {
  activityId?: number | string;
  activityName?: string;
  activityType?: ActivityType | any;
  startTime?: string;
  startTimeLocal?: string;
  distance?: number;
  elapsedDuration?: number;
  calories?: number;
  averageHeartRate?: number;
  [k: string]: any;
};

export type HealthEntry = {
  date?: string;
  heartRate?: number;
  steps?: number;
  sleepMinutes?: number;
  stressLevel?: number;
  calories?: number;
  [k: string]: any;
};

type GarminContext = {
  activities: Activity[];
  healthData: HealthEntry[];
  isLoading: boolean;
  error: string | null;
  refreshData: () => Promise<void>;
};

const GarminDataContext = createContext<GarminContext | undefined>(undefined);

export const GarminDataProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [healthData, setHealthData] = useState<HealthEntry[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const api = axios.create({
    // Relative baseURL so it works in dev and production (Express or Flask)
    baseURL: '',
    timeout: 10000,
  });

  const fetchAll = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [activitiesRes, healthRes] = await Promise.all([
        api.get('/api/garmin/activities'),
        api.get('/api/garmin/health'),
      ]);

      // Expect responses to contain the arrays in activities/healthData keys
      const a = activitiesRes?.data?.activities ?? activitiesRes?.data ?? [];
      const h = healthRes?.data?.healthData ?? healthRes?.data ?? [];

      setActivities(Array.isArray(a) ? a : []);
      setHealthData(Array.isArray(h) ? h : []);
    } catch (err: any) {
      const msg = err?.response?.data?.message || err?.message || 'Failed to fetch Garmin data';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Try to trigger backend refresh endpoint if available
      await api.post('/api/garmin/refresh').catch(() => undefined);
      // Re-fetch data after refresh
      await fetchAll();
    } catch (err: any) {
      const msg = err?.response?.data?.message || err?.message || 'Failed to refresh data';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let mounted = true;
    // Fetch on mount
    (async () => {
      if (!mounted) return;
      await fetchAll();
    })();

    return () => {
      mounted = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <GarminDataContext.Provider value={{ activities, healthData, isLoading, error, refreshData }}>
      {children}
    </GarminDataContext.Provider>
  );
};

export const useGarminData = (): GarminContext => {
  const ctx = useContext(GarminDataContext);
  if (!ctx) {
    throw new Error('useGarminData must be used within a GarminDataProvider');
  }
  return ctx;
};

export default GarminDataContext;

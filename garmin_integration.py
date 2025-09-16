#!/usr/bin/env python3
"""
Garmin Connect Integration Script
This script demonstrates how to connect to Garmin Connect and fetch real data.
"""

import os
import json
from datetime import datetime, timedelta
from garminconnect import Garmin
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_garmin():
    """Connect to Garmin Connect using credentials from environment variables"""
    email = os.getenv('GARMIN_EMAIL')
    password = os.getenv('GARMIN_PASSWORD')
    
    if not email or not password:
        print("❌ Please set GARMIN_EMAIL and GARMIN_PASSWORD in your .env file")
        return None
    
    try:
        print("🔐 Connecting to Garmin Connect...")
        garmin = Garmin(email, password)
        garmin.login()
        print("✅ Successfully connected to Garmin Connect!")
        return garmin
    except Exception as e:
        print(f"❌ Failed to connect to Garmin Connect: {str(e)}")
        return None

def fetch_activities(garmin, limit=10):
    """Fetch recent activities from Garmin Connect"""
    try:
        print(f"📊 Fetching last {limit} activities...")
        
        # Get activities for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        activities = garmin.get_activities_by_date(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # Sort by date and limit results
        activities = sorted(activities, key=lambda x: x['startTimeLocal'], reverse=True)[:limit]
        
        print(f"✅ Found {len(activities)} activities")
        return activities
        
    except Exception as e:
        print(f"❌ Failed to fetch activities: {str(e)}")
        return []

def fetch_health_data(garmin, days=7):
    """Fetch health data from Garmin Connect"""
    try:
        print(f"💓 Fetching health data for last {days} days...")
        
        health_data = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            try:
                # Get daily summary
                daily_summary = garmin.get_daily_summary(date)
                
                # Get heart rate data
                heart_rate_data = garmin.get_heart_rates(date)
                
                # Get sleep data
                sleep_data = garmin.get_sleep_data(date)
                
                health_entry = {
                    'date': date,
                    'steps': daily_summary.get('steps', 0),
                    'calories': daily_summary.get('calories', 0),
                    'distance': daily_summary.get('distance', 0),
                    'heartRate': heart_rate_data.get('restingHeartRate', 0) if heart_rate_data else 0,
                    'sleepMinutes': sleep_data.get('sleepTimeSeconds', 0) // 60 if sleep_data else 0,
                    'stressLevel': daily_summary.get('stressLevel', 0)
                }
                
                health_data.append(health_entry)
                
            except Exception as e:
                print(f"⚠️  Could not fetch data for {date}: {str(e)}")
                continue
        
        print(f"✅ Fetched health data for {len(health_data)} days")
        return health_data
        
    except Exception as e:
        print(f"❌ Failed to fetch health data: {str(e)}")
        return []

def save_data_to_file(data, filename):
    """Save data to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"💾 Data saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save data: {str(e)}")

def main():
    """Main function to demonstrate Garmin Connect integration"""
    print("🏃‍♂️ Garmin Connect Integration Demo")
    print("=" * 40)
    
    # Connect to Garmin
    garmin = connect_to_garmin()
    if not garmin:
        return
    
    # Fetch activities
    activities = fetch_activities(garmin, limit=20)
    if activities:
        save_data_to_file(activities, 'garmin_activities.json')
        
        # Print summary
        print("\n📊 Activity Summary:")
        for activity in activities[:5]:  # Show first 5
            print(f"  • {activity.get('activityName', 'Unknown')} - {activity.get('activityType', {}).get('typeKey', 'Unknown')} - {activity.get('startTimeLocal', 'Unknown date')}")
    
    # Fetch health data
    health_data = fetch_health_data(garmin, days=7)
    if health_data:
        save_data_to_file(health_data, 'garmin_health.json')
        
        # Print summary
        print("\n💓 Health Summary:")
        for data in health_data[:3]:  # Show first 3 days
            print(f"  • {data['date']}: {data['steps']} steps, {data['calories']} cal, {data['heartRate']} bpm")
    
    print("\n✅ Integration demo completed!")
    print("\nTo use this data in your web app:")
    print("1. Copy the JSON files to your server directory")
    print("2. Update your API endpoints to serve this data")
    print("3. Or modify garmin_fetcher.py to use real Garmin data")

if __name__ == '__main__':
    main()

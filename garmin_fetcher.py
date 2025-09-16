#!/usr/bin/env python3
"""
Garmin Connect Data Fetcher
This script fetches data from Garmin Connect and serves it via a simple HTTP server.
"""

import os
import json
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Garmin Connect integration
import random
from datetime import datetime, timedelta
from garminconnect import Garmin

# Global Garmin client
garmin_client = None

def connect_to_garmin():
    """Connect to Garmin Connect using credentials from environment variables"""
    global garmin_client
    
    email = os.getenv('GARMIN_EMAIL')
    password = os.getenv('GARMIN_PASSWORD')
    
    if not email or not password or email == 'your_email@example.com':
        logger.warning("Garmin credentials not set or using example values. Using mock data.")
        return None
    
    try:
        logger.info("🔐 Connecting to Garmin Connect...")
        garmin_client = Garmin(email, password)
        garmin_client.login()
        logger.info("✅ Successfully connected to Garmin Connect!")
        return garmin_client
    except Exception as e:
        logger.error(f"❌ Failed to connect to Garmin Connect: {str(e)}")
        logger.warning("Falling back to mock data.")
        return None

def fetch_real_activities(limit=20):
    """Fetch real activities from Garmin Connect"""
    if not garmin_client:
        return []
    
    try:
        logger.info(f"📊 Fetching last {limit} activities from Garmin Connect...")
        
        # Get activities for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        activities = garmin_client.get_activities_by_date(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # Sort by date and limit results
        activities = sorted(activities, key=lambda x: x.get('startTimeLocal', ''), reverse=True)[:limit]
        
        logger.info(f"✅ Found {len(activities)} real activities from Garmin Connect")
        return activities
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch real activities: {str(e)}")
        return []

def fetch_real_health_data(days=30):
    """Fetch real health data from Garmin Connect"""
    if not garmin_client:
        return []
    
    try:
        logger.info(f"💓 Fetching health data for last {days} days from Garmin Connect...")
        
        health_data = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            try:
                # Get daily summary
                daily_summary = garmin_client.get_daily_summary(date)
                
                # Get heart rate data
                heart_rate_data = garmin_client.get_heart_rates(date)
                
                # Get sleep data
                sleep_data = garmin_client.get_sleep_data(date)
                
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
                logger.warning(f"⚠️  Could not fetch data for {date}: {str(e)}")
                continue
        
        logger.info(f"✅ Fetched real health data for {len(health_data)} days from Garmin Connect")
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch real health data: {str(e)}")
        return []

def generate_mock_activities():
    """Generate realistic mock activities for the last 30 days"""
    activities = []
    activity_types = [
        {"typeKey": "running", "names": ["Morning Run", "Evening Jog", "Tempo Run", "Long Run", "Interval Training"]},
        {"typeKey": "cycling", "names": ["Road Cycling", "Mountain Biking", "Indoor Cycling", "Commute Ride", "Group Ride"]},
        {"typeKey": "swimming", "names": ["Pool Swim", "Open Water Swim", "Swim Training", "Aqua Jogging"]},
        {"typeKey": "walking", "names": ["Morning Walk", "Lunch Walk", "Evening Stroll", "Hiking"]},
        {"typeKey": "strength_training", "names": ["Weight Training", "CrossFit", "Bodyweight Workout", "Yoga"]}
    ]
    
    for i in range(30):
        activity_type = random.choice(activity_types)
        activity_date = datetime.now() - timedelta(days=i)
        
        # Skip some days randomly (not every day has activities)
        if random.random() < 0.3:  # 30% chance of no activity
            continue
            
        activity = {
            "activityId": i + 1,
            "activityName": random.choice(activity_type["names"]),
            "activityType": {"typeKey": activity_type["typeKey"]},
            "startTime": activity_date.isoformat() + "Z",
            "startTimeLocal": activity_date.isoformat(),
            "distance": random.randint(1000, 50000) if activity_type["typeKey"] in ["running", "cycling", "walking"] else random.randint(500, 3000),
            "elapsedDuration": random.randint(600, 7200),  # 10 minutes to 2 hours
            "calories": random.randint(200, 800),
            "averageHeartRate": random.randint(120, 180),
            "maxHeartRate": random.randint(150, 200)
        }
        activities.append(activity)
    
    return sorted(activities, key=lambda x: x["startTimeLocal"], reverse=True)

def generate_mock_health_data():
    """Generate realistic mock health data for the last 30 days"""
    health_data = []
    
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        
        # Generate realistic health metrics
        base_steps = random.randint(6000, 15000)
        base_calories = random.randint(1800, 2800)
        base_heart_rate = random.randint(60, 75)
        base_sleep = random.randint(360, 540)  # 6-9 hours in minutes
        base_stress = random.randint(15, 45)
        
        health_entry = {
            "date": date.strftime('%Y-%m-%d'),
            "heartRate": base_heart_rate,
            "steps": base_steps,
            "sleepMinutes": base_sleep,
            "stressLevel": base_stress,
            "calories": base_calories
        }
        health_data.append(health_entry)
    
    return sorted(health_data, key=lambda x: x["date"], reverse=True)

# Initialize data - try real Garmin data first, fall back to mock
def initialize_data():
    """Initialize data from Garmin Connect or generate mock data"""
    global MOCK_ACTIVITIES, MOCK_HEALTH_DATA
    
    # Try to connect to Garmin Connect
    connect_to_garmin()
    
    # Try to fetch real data
    real_activities = fetch_real_activities()
    real_health_data = fetch_real_health_data()
    
    if real_activities:
        MOCK_ACTIVITIES = real_activities
        logger.info("✅ Using real Garmin Connect activities data")
    else:
        MOCK_ACTIVITIES = generate_mock_activities()
        logger.info("📊 Using mock activities data")
    
    if real_health_data:
        MOCK_HEALTH_DATA = real_health_data
        logger.info("✅ Using real Garmin Connect health data")
    else:
        MOCK_HEALTH_DATA = generate_mock_health_data()
        logger.info("📊 Using mock health data")

# Initialize data on startup
initialize_data()

def refresh_data():
    """Refresh data from Garmin Connect or generate new mock data"""
    global MOCK_ACTIVITIES, MOCK_HEALTH_DATA
    
    # Try to refresh real data first
    real_activities = fetch_real_activities()
    real_health_data = fetch_real_health_data()
    
    if real_activities:
        MOCK_ACTIVITIES = real_activities
        logger.info("✅ Refreshed with real Garmin Connect activities data")
    else:
        MOCK_ACTIVITIES = generate_mock_activities()
        logger.info("📊 Refreshed with mock activities data")
    
    if real_health_data:
        MOCK_HEALTH_DATA = real_health_data
        logger.info("✅ Refreshed with real Garmin Connect health data")
    else:
        MOCK_HEALTH_DATA = generate_mock_health_data()
        logger.info("📊 Refreshed with mock health data")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Garmin Data Fetcher is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/garmin/activities', methods=['GET'])
def get_activities():
    """Get activities data"""
    try:
        # In a real implementation, you would:
        # 1. Authenticate with Garmin Connect
        # 2. Fetch activities from the API
        # 3. Process and return the data
        
        logger.info("Fetching activities data")
        
        # For now, return mock data
        return jsonify({
            "activities": MOCK_ACTIVITIES,
            "count": len(MOCK_ACTIVITIES),
            "lastUpdated": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching activities: {str(e)}")
        return jsonify({
            "error": "Failed to fetch activities",
            "message": str(e)
        }), 500

@app.route('/api/garmin/health', methods=['GET'])
def get_health_data():
    """Get health metrics data"""
    try:
        logger.info("Fetching health data")
        
        # For now, return mock data
        return jsonify({
            "healthData": MOCK_HEALTH_DATA,
            "count": len(MOCK_HEALTH_DATA),
            "lastUpdated": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching health data: {str(e)}")
        return jsonify({
            "error": "Failed to fetch health data",
            "message": str(e)
        }), 500

@app.route('/api/garmin/refresh', methods=['POST'])
def refresh_data_endpoint():
    """Refresh all data from Garmin Connect"""
    try:
        logger.info("🔄 Refreshing all data...")
        
        # Refresh data (real or mock)
        refresh_data()
        
        return jsonify({
            "message": "Data refreshed successfully",
            "timestamp": datetime.now().isoformat(),
            "activities_count": len(MOCK_ACTIVITIES),
            "health_data_count": len(MOCK_HEALTH_DATA),
            "data_source": "Garmin Connect" if garmin_client else "Mock Data"
        })
        
    except Exception as e:
        logger.error(f"Error refreshing data: {str(e)}")
        return jsonify({
            "error": "Failed to refresh data",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Garmin Data Fetcher on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

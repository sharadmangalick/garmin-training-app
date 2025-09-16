#!/usr/bin/env python3
"""
Simple Garmin Connect Test Script
Tests your Garmin Connect credentials and fetches some sample data.
"""

import os
from dotenv import load_dotenv

def test_garmin_connection():
    """Test the Garmin Connect connection"""
    print("🔐 Testing Garmin Connect connection...")
    
    # Load environment variables
    load_dotenv()
    
    email = os.getenv('GARMIN_EMAIL')
    password = os.getenv('GARMIN_PASSWORD')
    
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password) if password else 'Not set'}")
    
    if not email or not password or email == 'your_email@example.com':
        print("❌ Please update your .env file with your actual Garmin Connect credentials")
        print("\nEdit the .env file and change:")
        print("GARMIN_EMAIL=your_actual_email@example.com")
        print("GARMIN_PASSWORD=your_actual_password")
        return False
    
    try:
        from garminconnect import Garmin
        
        print(f"\nConnecting to Garmin Connect as: {email}")
        
        garmin = Garmin(email, password)
        garmin.login()
        
        print("✅ Successfully connected to Garmin Connect!")
        
        # Test fetching some data
        print("\n📊 Testing data fetch...")
        
        # Get recent activities
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        activities = garmin.get_activities_by_date(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        print(f"✅ Found {len(activities)} activities in the last 7 days")
        
        if activities:
            print("\nRecent activities:")
            for i, activity in enumerate(activities[:3]):  # Show first 3
                activity_name = activity.get('activityName', 'Unknown')
                activity_type = activity.get('activityType', {}).get('typeKey', 'Unknown')
                start_time = activity.get('startTimeLocal', 'Unknown')
                print(f"  {i+1}. {activity_name} ({activity_type}) - {start_time}")
        
        # Test health data
        print("\n💓 Testing health data...")
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            daily_summary = garmin.get_daily_summary(today)
            steps = daily_summary.get('steps', 0)
            calories = daily_summary.get('calories', 0)
            print(f"✅ Today's data: {steps} steps, {calories} calories")
        except Exception as e:
            print(f"⚠️  Could not fetch today's health data: {str(e)}")
        
        print("\n🎉 Garmin Connect integration is working!")
        print("You can now start the application with: python garmin_fetcher.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Double-check your email and password")
        print("2. Make sure you can log into Garmin Connect website")
        print("3. Check if your account has 2FA enabled (may need to disable)")
        print("4. Try logging out and back into Garmin Connect website")
        return False

if __name__ == '__main__':
    test_garmin_connection()

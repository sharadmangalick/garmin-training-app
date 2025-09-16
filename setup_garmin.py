#!/usr/bin/env python3
"""
Garmin Connect Setup Script
This script helps you set up your Garmin Connect credentials and test the connection.
"""

import os
import getpass
from dotenv import load_dotenv

def setup_garmin_credentials():
    """Interactive setup for Garmin Connect credentials"""
    print("🏃‍♂️ Garmin Connect Setup")
    print("=" * 40)
    print()
    
    # Load existing .env file if it exists
    load_dotenv()
    
    # Get current values
    current_email = os.getenv('GARMIN_EMAIL', '')
    current_password = os.getenv('GARMIN_PASSWORD', '')
    
    print("Please enter your Garmin Connect credentials:")
    print("(Press Enter to keep current values)")
    print()
    
    # Get email
    if current_email and current_email != 'your_email@example.com':
        email = input(f"Email [{current_email}]: ").strip()
        if not email:
            email = current_email
    else:
        email = input("Email: ").strip()
    
    # Get password
    if current_password and current_password != 'your_password':
        password = getpass.getpass(f"Password [{'*' * len(current_password)}]: ")
        if not password:
            password = current_password
    else:
        password = getpass.getpass("Password: ")
    
    # Validate inputs
    if not email or not password:
        print("❌ Email and password are required!")
        return False
    
    if email == 'your_email@example.com' or password == 'your_password':
        print("❌ Please use your actual Garmin Connect credentials!")
        return False
    
    # Update .env file
    env_content = f"""# Garmin Connect Credentials
GARMIN_EMAIL={email}
GARMIN_PASSWORD={password}

# Server Configuration
PORT=5001
NODE_ENV=development
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Credentials saved to .env file")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save credentials: {str(e)}")
        return False

def test_garmin_connection():
    """Test the Garmin Connect connection"""
    print("\n🔐 Testing Garmin Connect connection...")
    
    try:
        from garminconnect import Garmin
        from dotenv import load_dotenv
        
        load_dotenv()
        
        email = os.getenv('GARMIN_EMAIL')
        password = os.getenv('GARMIN_PASSWORD')
        
        if not email or not password:
            print("❌ No credentials found in .env file")
            return False
        
        print(f"Connecting as: {email}")
        
        garmin = Garmin(email, password)
        garmin.login()
        
        print("✅ Successfully connected to Garmin Connect!")
        
        # Test fetching some data
        print("📊 Testing data fetch...")
        activities = garmin.get_activities_by_date('2024-01-01', '2024-01-31')
        print(f"✅ Found {len(activities)} activities in January 2024")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your email and password")
        print("2. Make sure you have a Garmin Connect account")
        print("3. Try logging into Garmin Connect website first")
        print("4. Check if your account has 2FA enabled (may need to disable)")
        return False

def main():
    """Main setup function"""
    print("Welcome to the Garmin Training Dashboard setup!")
    print()
    
    # Setup credentials
    if not setup_garmin_credentials():
        print("\n❌ Setup failed. Please try again.")
        return
    
    # Test connection
    if test_garmin_connection():
        print("\n🎉 Setup complete! Your Garmin Training Dashboard is ready to use.")
        print("\nNext steps:")
        print("1. Start the Python backend: python garmin_fetcher.py")
        print("2. Start the React frontend: cd client && npm start")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print("\n⚠️  Setup completed but connection test failed.")
        print("The app will use mock data until you fix the connection.")

if __name__ == '__main__':
    main()

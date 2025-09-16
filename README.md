# Garmin Training Dashboard

A modern web application that pulls data from your Garmin Connect account and displays it in a more useful and visually appealing way.

## Features

- 📊 **Dashboard Overview**: Quick stats and metrics at a glance
- 📈 **Activity Trends**: Visual charts showing your training progress over time
- 💓 **Health Metrics**: Heart rate, steps, sleep, and stress data
- 📋 **Activity List**: Detailed view of your recent activities with filtering
- 🔄 **Real-time Updates**: Refresh data from your Garmin Connect account
- 📱 **Responsive Design**: Works great on desktop and mobile devices

## Tech Stack

- **Frontend**: React with TypeScript, Recharts for data visualization
- **Backend**: Node.js/Express for API server
- **Data Source**: Garmin Connect API (via Python garminconnect library)
- **Styling**: Modern CSS with responsive design

## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- Python 3.8 or higher
- A Garmin Connect account

### Installation

1. **Clone and install dependencies**:
   ```bash
   # Install Node.js dependencies
   npm run install-all
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your Garmin Connect credentials
   GARMIN_EMAIL=your_email@example.com
   GARMIN_PASSWORD=your_password
   ```

3. **Start the development servers**:
   ```bash
   # Start both frontend and backend (recommended)
   npm run dev
   
   # Or start them separately:
   # Backend (Node.js)
   npm run server
   
   # Frontend (React)
   npm run client
   
   # Python data fetcher (alternative backend)
   python garmin_fetcher.py
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Python API: http://localhost:5000 (if using Python backend)

## Garmin Connect Integration

### Option 1: Official Garmin Connect API (Recommended)
1. Visit [Garmin Developer Portal](https://developerportal.garmin.com/)
2. Apply for API access
3. Get your API credentials
4. Update the backend to use official API endpoints

### Option 2: Third-party Library (Current Implementation)
The app currently uses mock data. To connect to real Garmin data:

1. Install the garminconnect library: `pip install garminconnect`
2. Update `garmin_fetcher.py` to use real authentication
3. Replace mock data with actual API calls

### Option 3: Data Export
1. Export your data from Garmin Connect
2. Import the JSON/CSV files into the application
3. Process the data for visualization

## Project Structure

```
garmin-training-app/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── context/        # React context for state management
│   │   └── ...
├── server/                 # Node.js backend
│   └── index.js
├── garmin_fetcher.py       # Python data fetcher
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
└── README.md
```

## Available Scripts

- `npm run dev` - Start both frontend and backend
- `npm run server` - Start only the Node.js backend
- `npm run client` - Start only the React frontend
- `npm run build` - Build the React app for production
- `python garmin_fetcher.py` - Start the Python data fetcher

## Data Privacy

This application is designed to run locally on your machine. Your Garmin Connect credentials and data are not sent to any external servers. All data processing happens on your local machine.

## Troubleshooting

### Common Issues

1. **CORS errors**: Make sure both frontend and backend are running
2. **API connection issues**: Check your Garmin Connect credentials
3. **No data showing**: Verify your Garmin account has recent activities

### Getting Help

- Check the browser console for error messages
- Verify all services are running on the correct ports
- Ensure your Garmin Connect account has recent data

## Future Enhancements

- [ ] Real-time data synchronization
- [ ] Advanced analytics and insights
- [ ] Goal setting and tracking
- [ ] Social features and sharing
- [ ] Mobile app version
- [ ] Data export functionality
- [ ] Integration with other fitness platforms

## License

MIT License - feel free to use this project for personal or commercial purposes.

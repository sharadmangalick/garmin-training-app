const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from React app in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../client/build')));
}

// Routes
app.get('/api/health', (req, res) => {
  res.json({ message: 'Garmin Training App API is running!' });
});

// Garmin data routes
app.get('/api/garmin/activities', async (req, res) => {
  try {
    // TODO: Implement Garmin Connect data fetching
    res.json({ message: 'Activities endpoint - coming soon' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/garmin/health', async (req, res) => {
  try {
    // TODO: Implement health data fetching
    res.json({ message: 'Health data endpoint - coming soon' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Catch all handler for React routing
if (process.env.NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build/index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

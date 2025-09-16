import React from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import Header from './components/Header';
import { GarminDataProvider } from './context/GarminDataContext';

function App() {
  return (
    <GarminDataProvider>
      <div className="App">
        <Header />
        <main className="main-content">
          <Dashboard />
        </main>
      </div>
    </GarminDataProvider>
  );
}

export default App;

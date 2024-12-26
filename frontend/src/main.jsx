import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './components/HomePage';
import ElectivesPage from './components/ElectivesPage'
import SchedulePage from './components/SchedulePage'
import ManualCareersPage from './components/ManualCareersPage'
import SurveyPage from './components/SurveyPage'
import CareerResultsPage from './components/CareerResultsPage'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/electives" element={<ElectivesPage />} />
        <Route path="/schedule" element={<SchedulePage />} />
        <Route path="/manual-careers" element={<ManualCareersPage />} />
        <Route path="/survey-page" element={<SurveyPage />} />
        <Route path="/career-results" element={<CareerResultsPage />} />
        <Route path="/schedule" element={<SchedulePage />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

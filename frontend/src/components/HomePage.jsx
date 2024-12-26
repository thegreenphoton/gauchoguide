import React, { useEffect } from 'react';

import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './HomePage.css'

const HomePage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        console.log("Clearing data and restarting project...")
        localStorage.clear();
    }, []);

    const handleManualRoute = () => {
        localStorage.setItem('manualRoute', true);
        navigate('/manual-careers');
    };
    const handleSurveyRoute = () => {
        localStorage.setItem('manualRoute', false);
        navigate('/survey-page');
    }
    return (
        <div className="home-container">
            <header className="header">
                <h1 className="home-title">🎓 Gaucho Guide</h1>
                <h2 className="home-subtitle">Your Personalized Course Schedule Planner</h2>
            </header>
    
            <div className="hero-section">
                <p className="description">
                    Plan your courses, pick your dream careers, and graduate on time—effortlessly!
                </p>
            </div>
    
            <div className="options-container">
                <h3 className="options-header">Choose Your Path:</h3>
                <div className="button-container">
                    <button className="home-button" onClick={handleSurveyRoute}>
                        📋 Take the Survey
                    </button>
                    <button className="secondary-button" onClick={handleManualRoute}>
                        🎯 Pick Careers Manually
                    </button>
                </div>
            </div>
    
            <footer className="footer">
                <p>Built for UCSB students, by UCSB students. 🐻💙💛</p>
            </footer>
        </div>
    );

};

export default HomePage;
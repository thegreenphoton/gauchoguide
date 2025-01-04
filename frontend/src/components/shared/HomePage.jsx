import React, { useEffect, useState } from 'react';

import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import '../styles/HomePage.css'

const HomePage = () => {
    const navigate = useNavigate();
    const [selectedMajor , setSelectedMajor ] = useState('');
    const [errorMessage, setErrorMessage ] = useState('');

    useEffect(() => {
        console.log("Clearing data and restarting project...")
        localStorage.clear();
    }, []);

    const handleManualRoute = () => {
        if (selectedMajor) {
            localStorage.setItem('manualRoute', true);
            localStorage.setItem('selectedMajor', selectedMajor);
            navigate(`/${selectedMajor}/manual-careers`);
        }
        else {
            setErrorMessage('⚠️ Please select your major first!');
            //alert('Please select your major first!');
        }
    };

    const handleSurveyRoute = () => {
        if (selectedMajor) {
            localStorage.setItem('manualRoute', false);
            localStorage.setItem('selectedMajor', selectedMajor);
            navigate(`/${selectedMajor}/survey-page`);
        }
        else {
            setErrorMessage('⚠️ Please select your major first!');
            //alert('Please select your major first!');
        }

    };

    return (
        <div className="home-container">
            <header className="header">
                <h1 className="home-title">🎓 Gaucho Guide</h1>
                <h2 className="home-subtitle">Your Personalized Course Schedule Planner</h2>
            </header>
    
            <div className="hero-section">
                <p className="home-description">
                    Pick your dream careers, plan your courses, and graduate on time—effortlessly!
                </p>
            </div>
    
            <div className="options-container">
                <h3 className="options-header">Choose Your Major:</h3>

                <div className="major-selection-container">
                    <label htmlFor="major-select" className="major-label">
                        
                    </label>
                    <select
                        id="major-select"
                        className="major-dropdown"
                        value={selectedMajor}
                        onChange={(e) => {
                            setSelectedMajor(e.target.value);
                            setErrorMessage('');
                        }}
                    >
                        <option value="">-- Select Major --</option>
                        <option value="compsci">Computer Science</option>
                        <option value="ce">Computer Engineering</option>
                        <option value="ee">Electrical Engineering</option>
                        <option value="econ">Economics</option>
                        <option value="ecacc">Economics and Accounting</option>
                        <option value="sds">Statistics and Data Science</option>
                    </select>
                </div>

                {errorMessage && <p className="error-message">{errorMessage}</p>}

                <h3 className="options-header">Choose Your Path:</h3>
                <div className="button-container">
                    <button className="home-button" onClick={handleSurveyRoute}>
                        📋 Take the Survey
                    </button>
                    <button className="secondary-button" onClick={handleManualRoute}>
                        🎯 Pick Careers Manually
                    </button>
                </div>

                <div className="survey-note">
        <p>
            <strong>Note:</strong> The survey is intended to recommend you five careers in your field that align closest to your interests and goals. 
        </p>
    </div>
            </div>
    
            <footer className="footer">
                <p>Built for UCSB students, by Jay Udall (2027 Computer Engineering student).</p>
                <a href="https://www.linkedin.com/in/jayden-udall-926716253/">My LinkedIn</a>
            </footer>
        </div>
    );

};

export default HomePage;
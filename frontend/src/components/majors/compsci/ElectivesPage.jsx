import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../../styles/ElectivesPage.css';

const CSElectives = () => {
    const [electives, setElectives] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchElectives = async () => {
            try {
                const isManualRoute = JSON.parse(localStorage.getItem('manualRoute'));
    
                if (isManualRoute) {
                    // Manual route
                    const selectedCareers = JSON.parse(localStorage.getItem('selectedCareers'));
    
                    if (!Array.isArray(selectedCareers) || selectedCareers.length !== 5) {
                        console.error('Invalid selectedCareers format or length.');
                        alert('Invalid career data. Please re-select careers.');
                        return;
                    }
    
                    console.log('Sending Manual Route Data:', selectedCareers); 
    
                    // Send POST request with formatted careers
                    const response = await axios.post('http://127.0.0.1:8000/api/electives/', {
                        manualRoute: true,
                        selectedCareers: selectedCareers, 
                        major: "compsci"
                    });
                    localStorage.setItem('electives', JSON.stringify(response.data.electives));
    
                    setElectives(response.data.electives);
                    
                } else {
                    // Survey route
                    const exampleStudent = JSON.parse(localStorage.getItem('exampleStudent'));
    
                    if (!Array.isArray(exampleStudent) || exampleStudent.length !== 20) {
                        console.error('Invalid exampleStudent format or length.');
                        alert('Invalid survey data. Please retake the survey.');
                        return;
                    }
    
                    const response = await axios.post('http://127.0.0.1:8000/api/electives/', {
                        manualRoute: false,
                        exampleStudent: exampleStudent,
                        major: "compsci"
                    });
                    console.log('electives sent from electives page', response.data)
                    localStorage.setItem('electives', JSON.stringify(response.data.electives));

                    setElectives(response.data.electives);
                }
            } catch (error) {
                console.error('Error fetching electives:', error);
                alert('Failed to fetch electives.');
            }
        };
        fetchElectives();
    }, []);
    return (
        <div className="electives-page">
            

            <section className="electives-section">
                <h2>Major: Computer Science</h2>
                <h2>Your 14 Recommended Electives (ranked by relevance):</h2>
                <ul className="electives-list">
                    {electives.map((elective, index) => (
                        <li key={index} className="elective-item">
                            {elective.Course} 
                            <span className="relevance">Relevance: {Math.round(elective.Rescaled_Relevance)}%</span>
                        </li>
                    ))}
                </ul>
            </section>

            <div className="button-container">
                <button className="home-button" onClick={() => navigate('/')}>Return to Home</button>
                <button className="schedule-button" onClick={() => navigate('/schedule')}>View Schedule</button>
            </div>
        </div>
    );
};
export default CSElectives;
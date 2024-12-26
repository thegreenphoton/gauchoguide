import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './ElectivesPage.css';

const ElectivesPage = () => {
    const [electives, setElectives] = useState([]);
    const [sequences, setSequences] = useState([]);
    const [sequenceCourses, setSequenceCourses] = useState([]);
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
                    });
    
                    setElectives(response.data.topSixElectives);
                    setSequences(response.data.topTwoSequences);
                    setSequenceCourses(response.data.topSequenceCourses);
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
                    });
                    console.log('electives sent from electives page', response.data)
                    localStorage.setItem('topTwoSequences', JSON.stringify(response.data.topTwoSequences));
                    localStorage.setItem('topSequenceCourses', JSON.stringify(response.data.topSequenceCourses));
                    localStorage.setItem('topSixElectives', JSON.stringify(response.data.topSixElectives));

                    setElectives(response.data.topSixElectives);
                    setSequences(response.data.topTwoSequences);
                    setSequenceCourses(response.data.topSequenceCourses);
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
            <h1 className="title">Elective Recommendations</h1>

            <section className="sequences-section">
                <h2>Top 2 Sequences</h2>
                {sequences.map((sequence, index) => (
                    <div key={index} className="sequence-card">
                        <h3 className="sequence-title">{sequence.Sequence}</h3>
                        <ul className="course-list">
                            {sequenceCourses
                                .filter(course => course.Sequence === sequence.Sequence)
                                .map((course, i) => (
                                    <li key={i} className="course-item">{course.Course}</li>
                                ))}
                        </ul>    
                    </div>
                ))}
            </section>

            <section className="electives-section">
                <h2>Top 6 Electives</h2>
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
export default ElectivesPage;
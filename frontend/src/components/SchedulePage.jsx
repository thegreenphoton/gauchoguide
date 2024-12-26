import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SchedulePage.css';

const SchedulePage = () => {
    const navigate = useNavigate();
    const [schedule, setSchedule] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSchedule = async () => {
            try {
                // Check if manual or survey route
                const isManualRoute = JSON.parse(localStorage.getItem('manualRoute'));
        
                // Fetch data from localStorage
                const topTwoSequences = JSON.parse(localStorage.getItem('topTwoSequences'));
                const topSequenceCourses = JSON.parse(localStorage.getItem('topSequenceCourses'));
                const topSixElectives = JSON.parse(localStorage.getItem('topSixElectives'));
        
                let requestBody = {};
        
                if (isManualRoute) {
                    // Manual route - Get formatted careers
                    const selectedCareers = JSON.parse(localStorage.getItem('selectedCareers'));
        
                    requestBody = {
                        manualRoute: true,
                        selectedCareers,
                        topTwoSequences,
                        topSequenceCourses,
                        topSixElectives,
                    };
                } else {
                    // Survey route - Get exampleStudent
                    const exampleStudent = JSON.parse(localStorage.getItem('exampleStudent'));
        
                    requestBody = {
                        manualRoute: false,
                        exampleStudent,
                        topTwoSequences,
                        topSequenceCourses,
                        topSixElectives,
                    };
                }
        
                console.log("Sending Request Body:", requestBody); // Debugging log
        
                // Make API request
                const response = await axios.post('http://localhost:8000/api/schedule-builder/', requestBody);
        
                console.log("Schedule Response:", response.data); // Debugging log
        
                // Validate the schedule response format
                if (!response.data.schedule || !Array.isArray(response.data.schedule)) {
                    throw new Error("Invalid schedule format received from backend.");
                }
        
                // **FIX: Correct mapping of schedule data**
                const formattedSchedule = response.data.schedule.map(term => ({
                    term: term.term,
                    courses: term.courses,
                    difficulty: term.difficulty
                }));
                
        
                // Update state with the schedule
                setSchedule(formattedSchedule);
            } catch (error) {
                console.error('Error fetching schedule:', error);
                setError('Failed to fetch schedule. Please try again.');
            }
        };
        
        
        
        

        fetchSchedule();
    }, []);

    return (
        <div className="schedule-container">
            <h1>Your Course Schedule:</h1>
            <br></br>
            {error && <p className="error-message">{error}</p>}

            {schedule.length > 0 ? (
                <div className="schedule-grid">
                    {schedule.map((term, index) => (
                        <div key={index} className="term-card">
                            <h2>Quarter {term.term}</h2>
                            <ul className="course-list">
                                {term.courses.map((course, i) => (
                                    <li key={i} className="course-item">
                                        {course}
                                    </li>
                                ))}
                            </ul>
                            <p className="difficulty">Difficulty: {term.difficulty}</p>
                        </div>
                    ))}
                </div>
            ) : (
                <p>Loading schedule...</p>
            )}

            <div className="button-container">
                <button onClick={() => navigate('/electives')}>Back to Electives</button>
                <button onClick={() => navigate('/')}>Return to Home</button>

            </div>
        </div>
    );
};

export default SchedulePage;
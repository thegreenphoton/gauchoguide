import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/SchedulePage.css';

const SchedulePage = () => {
    const navigate = useNavigate();
    const [schedule, setSchedule] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSchedule = async () => {
            try {
                const major = localStorage.getItem('selectedMajor')
                // Check if manual or survey route
                const isManualRoute = JSON.parse(localStorage.getItem('manualRoute'));

                let requestBody = {}

                if (major == "ce") {
                                    // Fetch data from localStorage
                    const topTwoSequences = JSON.parse(localStorage.getItem('topTwoSequences'));
                    const topSequenceCourses = JSON.parse(localStorage.getItem('topSequenceCourses'));
                    const topSixElectives = JSON.parse(localStorage.getItem('topSixElectives'));
            
                    
            
                    if (isManualRoute) {
                        // Manual route - Get formatted careers
                        const selectedCareers = JSON.parse(localStorage.getItem('selectedCareers'));
            
                        requestBody = {
                            manualRoute: true,
                            major: major,
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
                            major: major,
                            exampleStudent,
                            topTwoSequences,
                            topSequenceCourses,
                            topSixElectives,
                        };
                    }

                }
                else {

                    const electives = JSON.parse(localStorage.getItem('electives'));
                    if (isManualRoute) {
                        // Manual route - Get formatted careers
                        const selectedCareers = JSON.parse(localStorage.getItem('selectedCareers'));
            
                        requestBody = {
                            manualRoute: true,
                            major: major,
                            selectedCareers,
                            electives

                        };
                    } else {
                        // Survey route - Get exampleStudent
                        const exampleStudent = JSON.parse(localStorage.getItem('exampleStudent'));
            
                        requestBody = {
                            manualRoute: false,
                            major: major,
                            exampleStudent,
                            electives
                        };
                    }

                }

                console.log("Sending Request Body:", requestBody); // Debugging log
        
                // Make API request
                //const response = await axios.post('http://localhost:8000/api/schedule-builder/', requestBody);
                const response = await axios.post(
                    `${import.meta.env.VITE_BACKEND_URL}/api/schedule-builder/`,
                    requestBody
                )
        
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

    const handleBack = () => {
        const major = localStorage.getItem('selectedMajor');
        if (major) {
            navigate(`/${major}/electives`)
        }
        else {
            console.error("no major found when going from schedule page to back")
            navigate(`/`)
        }
        
    };

    const getDifficultyClass = (difficulty) => {
        if (difficulty >= 8) {
            return 'difficulty-red';
        }
        else if (difficulty >= 6) {
            return 'difficulty-yellow';
        } 
        else if (difficulty >= 0) {
            return 'difficulty-green'
        }
        else {
            return '';
        }
    };

    return (
<div className="schedule-container">
    <h1>Your Upper-Division Schedule:</h1>
    <br></br>
    {error && <p className="error-message">{error}</p>}

    {schedule.length > 0 ? (
        <div className="schedule-grid">
            {schedule.map((term, index) => (
                <div key={index} className="term-card">
                    <h2>Quarter {term.term}</h2>
                    <ul className="course-list">
                        {term.courses.map((course, i) => (
                            <li 
                                key={i} 
                                className={`course-item ${getDifficultyClass(course.difficulty)}`}
                            >
                                {course.course} (Difficulty: {course.difficulty}/10)
                            </li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    ) : (
        <p>Loading schedule...</p>
    )}

    <div className="button-container">
        <button onClick={handleBack}>Back to Electives</button>
        <button onClick={() => navigate('/')}>Return to Home</button>
    </div>

    <div className="difficulty-note">
        <p>
            <strong>Note:</strong> Course difficulties are calculated based heavily on past grade distributions and conceptual difficulty ratings, with some influence from failure rates 
            and variability in performance. Use this information as a guide, but consider your own strengths and interests.
        </p>
    </div>

    <div className="schedule-note">
        <p>
            <strong>Note:</strong> This schedule was based on UCSB's 2024-25 GEAR publications, major requirements, prerequisite requirements, and course offering schedule from each department. Prerequisites are usually handled accurately, 
            but mistakes <strong>can be made</strong>. Double check before scheduling to ensure all necessary prerequisites have been taken prior. 
        </p>
    </div>
</div>
    );
};

export default SchedulePage;
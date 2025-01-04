import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../styles/ManualCareersPage.css';

const CSManual = () => {
    const navigate = useNavigate();
    const allCareers = [
        'Software Engineer (Back-End)',
        'Data Scientist',
        'Machine Learning Engineer',
        'Cybersecurity Analyst',
        'Cloud Engineer',
        'DevOps Engineer',
        'Systems Analyst',
        'Database Administrator',
        'Game Developer',
        'Mobile App Developer',
        'AI Specialist',
        'Software Engineer (Front-End)',
        'Network Administrator/Engineer',
        'Software Developer',
        'Computer Vision Engineer'
    ];
    const [availableCareers, setAvailableCareers] = useState(allCareers);
    const [selectedCareers, setSelectedCareers] = useState([]);

    const handleSelectedCareers = (career) => {
        if (selectedCareers.length < 5 && !selectedCareers.includes(career)) {
            setSelectedCareers([...selectedCareers, career]);
            setAvailableCareers(availableCareers.filter((c) => c !== career));
        }
    };

    const handleRemoveCareer = (career) => {
        setSelectedCareers(selectedCareers.filter((c) => c !== career));
        setAvailableCareers([...availableCareers, career]);
    };

    const handleSubmit = async () => {
        const weights = [0.50, 0.20, 0.10, 0.10, 0.10];
    
        // Format careers for backend
        const formattedCareers = selectedCareers.map((career, index) => ({
            career: career,
            relevance: 30.0, // Default relevance for manual route
            weight: weights[index], // Assign predefined weights
        }));
    
        console.log("Formatted Careers:", formattedCareers); // Debugging
    
        // Save formatted careers to localStorage
        localStorage.setItem('selectedCareers', JSON.stringify(formattedCareers)); 
    
        try {
            const response = await axios.post('http://localhost:8000/api/electives/', {
                manualRoute: true,
                selectedCareers: formattedCareers, // Send formatted data
                major: "compsci"
            });
    
            // Save results
            localStorage.setItem('electives', JSON.stringify(response.data.electives));
    
            navigate('/compsci/electives');
        } catch (error) {
            console.error('Error submitting selection:', error);
            alert('Failed to fetch electives. Please try again.');
        }
    };

    return (
        <div className="manual-careers-container">
            <h1 className="title">Select Your Top 5 Careers</h1>
            <p className="description">Choose your top 5 careers in order of preference.</p>

            <div className="career-selection">
                <div className="available-careers">
                    <h2>Available Careers:</h2>
                    <ul className="careers-list">
                        {availableCareers.map((career, index) => (
                            <li key={index} className="career-item">
                                {career}
                                <button
                                    className="select-button"
                                    disabled={selectedCareers.includes(career) || selectedCareers.length >= 5}
                                    onClick={() => handleSelectedCareers(career)}
                                >
                                    Select
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="selected-careers">
                    <h2>Selected Careers:</h2>
                    <ul className="selected-list">
                        {selectedCareers.map((career, index) => (
                            <li key={index} className="selected-item">
                                {index + 1}. {career}
                                <button
                                    className="remove-button"
                                    onClick={() => handleRemoveCareer(career)}
                                >
                                    Remove
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            <div className="buttons-container">
                <button
                    className="submit-button"
                    onClick={handleSubmit}
                    disabled={selectedCareers.length !== 5}
                >
                    Submit Careers
                </button>
                <button className="back-button" onClick={() => navigate(-1)}>
                    Back
                </button>
            </div>
        </div>
    );
};

export default CSManual;
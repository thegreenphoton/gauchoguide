import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../styles/ManualCareersPage.css';

const CEManual = () => {
    const navigate = useNavigate();
    const allCareers = [
        'Software Engineer', 
        'Embedded Systems Engineer', 
        'Hardware Engineer', 
        'Machine Learning Engineer', 
        'FPGA Engineer',
        'Robotics Engineer', 
        'Network Engineer',
        'Electrical Engineer', 
        'Cybersecurity Engineer', 
        'VLSI Design Engineer',
        'ASIC Design Engineer',
        'Data Engineer',
        'AI Research Scientist', 
        'Cloud Architect',
        'DevOps Engineer',
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
                major: "ce",
            });
    
            // Save results
            localStorage.setItem('topTwoSequences', JSON.stringify(response.data.topTwoSequences));
            localStorage.setItem('topSequenceCourses', JSON.stringify(response.data.topSequenceCourses));
            localStorage.setItem('topSixElectives', JSON.stringify(response.data.topSixElectives));
    
            navigate('/ce/electives');
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

export default CEManual;
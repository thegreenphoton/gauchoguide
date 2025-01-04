import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/CareerResultsPage.css';

const CareerResultsPage = () => {
    const [results, setResults] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const storedResults = localStorage.getItem('topCareers');
        const storedMajor = localStorage.getItem('selectedMajor');

        if (storedResults) {
            try {
                const parsedResults = JSON.parse(storedResults);
                setResults(parsedResults); 
            } catch (error) {
                console.error("Failed to parse stored results:", error);
            }
        } else {
            console.error("No results found in localStorage.");
        }
    }, []);

    const handleNavigateToElectives = () => {
        const major = localStorage.getItem('selectedMajor'); // Get the selected major
        
        if (major) {
            // Navigate to the major-specific electives page
            navigate(`/${major}/electives`);
        } else {
            // Fallback to a default electives page
            console.error('No major selected. Navigating to default electives page.');
            navigate('/electives');
        }
    };

    return (
        <div className="results-container">
            <h1>Your Top 5 Careers</h1>
            <p>Based on your survey responses, here are your recommended career paths:</p>
            
            <ul className="results-list">
                {results.map((career, index) => (
                    <li key={index}>
                        {index + 1}. {career.career} - Score: {career.relevance ? `${career.relevance}` : 'N/A'}
%
                    </li>
                ))}
            </ul>

            <div className="results-buttons">
                <button 
                    onClick={() => navigate('/')}
                    className="results-button home"
                >
                    Return to Home
                </button>
                <button 
                    onClick={handleNavigateToElectives}
                    className="results-button electives"
                >
                    View Electives
                </button>

            </div>
        </div>
    );
};

export default CareerResultsPage;

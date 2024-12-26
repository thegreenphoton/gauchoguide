import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CareerResultsPage.css';

const CareerResultsPage = () => {
    const [results, setResults] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const storedResults = localStorage.getItem('topCareers');
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
                    onClick={() => navigate('/electives')}
                    className="results-button electives"
                >
                    View Electives
                </button>
                <button 
                    onClick={() => navigate('/')}
                    className="results-button home"
                >
                    Return to Home
                </button>
            </div>
        </div>
    );
};

export default CareerResultsPage;

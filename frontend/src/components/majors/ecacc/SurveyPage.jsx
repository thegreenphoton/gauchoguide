import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
//import './components/majors/ecacc/SurveyPage.css';
import '../../styles/SurveyPage.css';

const EcaccSurvey = () => {
    const navigate = useNavigate();
    const [responses, setResponses] = useState(Array(20).fill(3)); 

    const questions = [
        'A high salary is one of the most important factors in my career choice.',
        'Work-life balance is crucial to me when choosing a career.',
        'I enjoy working in teams and collaborating with others on projects.',
        'I prefer a role that allows me to work on a variety of different tasks and projects.',
        'I would prefer a career in an established, traditional field rather than a rapidly changing industry.',
        'I am comfortable with the idea of working in an industry that may change significantly due to advancements in technology.',
        'I am comfortable with roles where I have to work independently and make my own decisions.',
        'Having flexibility in my work schedule, such as remote work options, is very important to me.',
        'I am interested in a role that requires deep specialization rather than broad knowledge.',
        'I would consider taking on a career path that has the potential to be impacted by AI or automation in the future.',
        'I enjoy analyzing financial data to identify trends and make forecasts.',
        'I am interested in preparing and reviewing financial statements for accuracy and compliance.',
        'I find satisfaction in developing budgets and monitoring expenses to ensure financial stability.',
        'I enjoy identifying and assessing financial risks to help organizations make informed decisions.',
        'I am passionate about ensuring compliance with tax laws and regulations while preparing tax returns.',
        'I like investigating financial discrepancies and conducting audits to detect errors or fraud.',
        'I enjoy working with accounting software and systems to streamline financial reporting.',
        'I am interested in evaluating investment opportunities and conducting market research.',
        'I find it rewarding to develop strategies for reducing costs and improving financial efficiency.',
        'I am comfortable presenting financial data and recommendations to executives and stakeholders.'
    ]

    const handleResponseChange = (index, value) => {
        const updatedResponses = [...responses];
        updatedResponses[index] = value;
        setResponses(updatedResponses);
    };

    const submitSurvey = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/career-results/', {
                manualRoute: false,
                exampleStudent: responses,
                major: "ecacc"
            });
            localStorage.setItem('exampleStudent', JSON.stringify(response.data.exampleStudent));
            localStorage.setItem('topCareers', JSON.stringify(response.data.topCareers));
            navigate('/career-results');
        } catch (error) {
            console.error('Error calculating careers:', error);
        }
    };

    return (
        <div className="survey-container">
            <h1>Survey</h1>
            <p>Please select the option that best represents your opinion:</p>
            <div className="survey-form">
                {questions.map((question, index) => (
                    <div key={index} className="question-container">
                        <p className="question">{question}</p>
                        <div className="options">
                            {['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'].map((label, value) => (
                                <button
                                    key={value}
                                    className={`option-button ${responses[index] === value + 1 ? 'selected' : ''}`}
                                    onClick={() => handleResponseChange(index, value + 1)}
                                >
                                    {label}
                                </button>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
            <div className="buttons-container">
                <button onClick={() => navigate(-1)} className="back-button">Back</button>
                <button onClick={submitSurvey} className="submit-button">Submit</button>
            
            </div>
        </div>
    );
};

export default EcaccSurvey;
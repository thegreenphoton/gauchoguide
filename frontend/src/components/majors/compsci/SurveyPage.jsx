import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../styles/SurveyPage.css';

const CSSurvey = () => {
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
        'I enjoy breaking down complex problems into smaller, manageable parts and developing algorithms to solve them.',
        'I am interested in working with data sets to extract meaningful insights and build predictive models.',
        'I am excited about designing and implementing machine learning algorithms to make systems smarter and more autonomous.',
        'I am passionate about identifying and mitigating security vulnerabilities in systems and networks.',
        'I enjoy working with cloud platforms (e.g., AWS, Azure, Google Cloud) to deploy and manage scalable applications.',
        'I enjoy coding, debugging, and optimizing applications across different programming languages and frameworks.',
        'I am interested in automating software deployment and streamlining development workflows.',
        'I enjoy designing and building interactive applications, games, or mobile apps for user engagement.',
        'I like configuring and managing computer networks or analyzing system requirements to improve performance.',
        'I find it exciting to develop AI-based solutions for image recognition, facial detection, or autonomous systems.'
    ]

    const handleResponseChange = (index, value) => {
        const updatedResponses = [...responses];
        updatedResponses[index] = value;
        setResponses(updatedResponses);
    };

    const submitSurvey = async () => {
        try {
            const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/career-results/`, {
                manualRoute: false,
                exampleStudent: responses,
                major: "compsci"
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

export default CSSurvey;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../styles/SurveyPage.css';

const SdsSurvey = () => {
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
        'I enjoy analyzing large datasets to identify patterns and trends.',
        'I am interested in building predictive models to make data-driven decisions.',
        'I find satisfaction in visualizing data to communicate insights effectively.',
        'I enjoy programming in languages such as Python, R, or SQL to manipulate and analyze data.',
        'I am passionate about developing machine learning algorithms for pattern recognition and automation.',
        'I like creating dashboards and reports to monitor key business metrics.',
        'I enjoy designing experiments and performing statistical tests to validate hypotheses.',
        'I find it exciting to work with cloud-based data storage and computing platforms.',
        'I am interested in evaluating and mitigating risks through data modeling and simulations.',
        'I like applying mathematical models and optimization techniques to solve complex problems.'
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
                major: "sds"
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

export default SdsSurvey;
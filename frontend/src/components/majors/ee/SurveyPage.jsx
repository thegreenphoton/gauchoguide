import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../styles/SurveyPage.css';

const EESurvey = () => {
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
        'I enjoy designing and analyzing electrical circuits and systems for various applications.',
        'I am interested in developing and testing embedded systems for hardware devices.',
        'I find satisfaction in working with power systems and renewable energy technologies.',
        'I enjoy programming microcontrollers and designing control systems for automation.',
        'I am passionate about working with communication technologies such as wireless networks and RF systems.',
        'I like solving problems related to signal processing, filtering, and data transmission.',
        'I am excited about designing and developing microelectronics and integrated circuits.',
        'I enjoy creating and testing prototypes for hardware systems and electronic devices.',
        'I find it rewarding to optimize manufacturing processes and improve system automation.',
        'I am interested in researching and implementing VLSI (Very Large Scale Integration) designs.'
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
                major: "ee"
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

export default EESurvey;
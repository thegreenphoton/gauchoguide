import numpy as np 
from numpy import dot
from numpy.linalg import norm

def normalize_scores(scores):
    min_score = min(scores.values())
    max_score = max(scores.values())
    return {career: (score - min_score) / (max_score - min_score) for career, score in scores.items()}

def cosine_similarity(student, career):
    return dot(student, career) / (norm(student) * norm(career))

def calculate_weighted_similarity(student, major):

    career_scores = {
"ce": {
    "Software Engineer" : np.array([4, 3, 4, 4, 2, 5, 4, 5, 3, 4, 5, 2, 1, 2, 5, 1, 3, 3, 3, 2]),
    "Embedded Systems Engineer" : np.array([3, 3, 4, 3, 4, 3, 4, 2, 5, 3, 4, 2, 5, 2, 4, 5, 2, 3, 5, 1]),
    "Hardware Engineer" : np.array([3, 3, 4, 3, 4, 3, 4, 2, 5, 2, 2, 3, 5, 1, 3, 5, 1, 2, 3, 1]),
    "Machine Learning Engineer" : np.array([5, 3, 4, 4, 2, 5, 4, 4, 5, 5, 5, 5, 1, 2, 5, 1, 5, 3, 3, 5]),
    "FPGA Engineer" : np.array([4, 3, 4, 3, 4, 3, 5, 3, 5, 3, 4, 3, 5, 2, 5, 5, 3, 2, 5, 2]), 
    "Robotics Engineer" : np.array([3, 3, 4, 5, 3, 5, 4, 2, 4, 5, 4, 3, 5, 2, 4, 5, 4, 2, 4, 3]),
    "Network Engineer" : np.array([2, 3, 4, 4, 4, 4, 4, 3, 4, 3, 2, 3, 2, 5, 3, 5, 2, 5, 3, 1]),
    "Electrical Engineer" : np.array([4, 3, 4, 3, 5, 2, 4, 3, 5, 3, 3, 2, 5, 2, 4, 5, 3, 2, 4, 2]), 
    "Cybersecurity Engineer" : np.array([4, 3, 4, 4, 2, 5, 4, 3, 4, 4, 3, 4, 2, 5, 3, 3, 3, 5, 4, 2]),
    "VLSI Design Engineer" : np.array([5, 3, 4, 3, 4, 4, 3, 2, 5, 3, 3, 3, 5, 1, 4, 4, 2, 2, 3, 2]),
    "ASIC Design Engineer" : np.array([5, 3, 3, 3, 5, 3, 4, 3, 5, 2, 3, 3, 5, 2, 5, 5, 2, 2, 4, 2]), 
    "Data Engineer" : np.array([4, 4, 4, 4, 3, 5, 4, 4, 4, 4, 5, 3, 1, 3, 4, 2, 3, 4, 3, 2]),
    "AI Research Scientist" : np.array([5, 3, 4, 4, 2, 5, 4, 4, 5, 5, 4, 5, 1, 2, 5, 2, 5, 3, 3, 5]),
    "Cloud Architect" : np.array([5, 4, 4, 4, 3, 5, 4, 4, 4, 4, 4, 3, 1, 5, 4, 2, 3, 5, 4, 2]),
    "DevOps Engineer" : np.array([4, 3, 5, 5, 2, 5, 4, 4, 4, 5, 4, 3, 1, 4, 4, 2, 2, 5, 4, 1]),
},
"compsci": {
    "Software Engineer (Back-End)": np.array([4, 3, 4, 4, 2, 5, 4, 5, 3, 4, 5, 2, 1, 2, 5, 5, 4, 3, 3, 4]),
    "Data Scientist": np.array([4, 3, 3, 4, 3, 4, 4, 4, 5, 3, 4, 5, 5, 2, 4, 4, 3, 2, 2, 5]),
    "Machine Learning Engineer": np.array([4, 3, 3, 4, 2, 5, 4, 4, 5, 3, 4, 5, 5, 2, 4, 4, 3, 3, 2, 5]),
    "Cybersecurity Analyst": np.array([4, 4, 4, 3, 3, 5, 3, 3, 3, 3, 4, 3, 2, 5, 3, 3, 2, 2, 5, 2]),
    "Cloud Engineer": np.array([4, 3, 4, 4, 2, 5, 4, 5, 4, 3, 4, 3, 3, 3, 5, 4, 5, 3, 2, 4]),
    "DevOps Engineer": np.array([4, 3, 4, 5, 2, 5, 4, 4, 3, 3, 4, 3, 2, 3, 5, 4, 5, 3, 2, 3]),
    "Systems Analyst": np.array([3, 4, 4, 4, 4, 4, 3, 4, 3, 3, 4, 3, 2, 3, 4, 3, 3, 2, 3, 2]),
    "Database Administrator": np.array([4, 4, 3, 3, 4, 3, 3, 4, 4, 3, 3, 3, 2, 3, 4, 3, 2, 2, 4, 2]),
    "Game Developer": np.array([3, 4, 4, 4, 2, 4, 4, 4, 4, 3, 4, 3, 2, 2, 3, 5, 4, 5, 2, 4]),
    "Mobile App Developer": np.array([3, 4, 4, 4, 2, 4, 4, 4, 4, 3, 4, 3, 2, 2, 3, 5, 4, 5, 2, 4]),
    "AI Specialist": np.array([4, 3, 3, 4, 2, 5, 4, 4, 5, 3, 4, 5, 5, 2, 4, 4, 3, 2, 2, 5]),
    "Software Engineer (Front-End)": np.array([4, 3, 4, 4, 2, 4, 4, 5, 3, 4, 5, 2, 1, 2, 4, 5, 5, 3, 3, 4]),
    "Network Administrator/Engineer": np.array([3, 4, 4, 3, 4, 4, 3, 3, 3, 3, 3, 3, 2, 4, 3, 3, 2, 2, 5, 2]),
    "Software Developer": np.array([4, 3, 4, 4, 2, 5, 4, 5, 3, 4, 5, 2, 1, 2, 5, 5, 4, 3, 3, 4]),
    "Computer Vision Engineer": np.array([4, 3, 3, 4, 2, 5, 4, 4, 5, 3, 4, 5, 5, 2, 4, 4, 3, 2, 2, 5]),
},
"ee": {
    "Electrical Engineer": np.array([5, 3, 4, 4, 5, 4, 3, 3, 4, 4, 5, 4, 5, 4, 3, 4, 4, 4, 4, 4]),
    "Electronics Engineer": np.array([4, 3, 4, 4, 5, 4, 3, 3, 4, 4, 4, 4, 3, 4, 4, 4, 5, 4, 4, 5]),
    "Power Systems Engineer": np.array([4, 3, 4, 3, 5, 4, 3, 3, 4, 3, 5, 3, 5, 3, 3, 4, 3, 3, 5, 3]),
    "Control Systems Engineer": np.array([4, 3, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 5, 3, 4, 4, 4, 5, 4]),
    "Telecommunications Engineer": np.array([4, 3, 4, 4, 4, 5, 3, 3, 4, 4, 4, 4, 3, 4, 5, 5, 4, 3, 3, 4]),
    "RF (Radio Frequency) Engineer": np.array([4, 3, 3, 4, 4, 5, 3, 3, 4, 4, 3, 4, 3, 4, 5, 5, 4, 3, 3, 4]),
    "Embedded Systems Engineer": np.array([4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 5, 3, 5, 3, 4, 5, 4, 3, 4]),
    "Hardware Engineer": np.array([4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 3, 4, 3, 4, 5, 4, 3, 4]),
    "Signal Processing Engineer": np.array([4, 3, 4, 4, 4, 5, 3, 3, 4, 4, 4, 4, 3, 4, 5, 5, 4, 3, 3, 4]),
    "Software Engineer": np.array([4, 3, 4, 5, 3, 5, 4, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4, 3, 4]),
    "Microelectronics Engineer": np.array([4, 3, 3, 4, 4, 4, 3, 3, 5, 4, 4, 4, 3, 4, 3, 4, 5, 4, 4, 5]),
    "Renewable Energy Engineer": np.array([4, 3, 4, 3, 5, 4, 3, 3, 4, 4, 5, 3, 5, 3, 3, 4, 3, 3, 5, 3]),
    "Automation Engineer": np.array([4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 5, 3, 4, 4, 4, 5, 4]),
    "Manufacturing Engineer": np.array([4, 3, 4, 4, 5, 4, 3, 3, 4, 4, 4, 3, 5, 3, 3, 4, 3, 3, 5, 4]),
    "VLSI Design Engineer": np.array([4, 3, 3, 4, 4, 4, 3, 3, 5, 4, 4, 4, 3, 4, 3, 4, 5, 4, 4, 5]),
},
"econ": {
    "Financial Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 5, 4, 4, 5, 4, 4, 5, 4, 5, 4]),
    "Economic Consultant": np.array([4, 4, 4, 4, 4, 5, 3, 4, 4, 4, 5, 5, 4, 5, 5, 3, 4, 5, 4, 5]),
    "Market Research Analyst": np.array([4, 4, 5, 4, 4, 5, 3, 4, 4, 4, 4, 5, 5, 4, 4, 3, 4, 5, 3, 4]),
    "Data Analyst": np.array([4, 4, 4, 3, 4, 5, 3, 4, 4, 4, 5, 5, 5, 4, 4, 4, 4, 4, 3, 4]),
    "Policy Analyst": np.array([4, 3, 4, 3, 4, 4, 3, 4, 4, 4, 5, 5, 4, 5, 5, 4, 4, 5, 4, 5]),
    "Actuary": np.array([5, 3, 3, 3, 4, 4, 3, 3, 5, 5, 5, 4, 5, 4, 4, 5, 5, 4, 4, 5]),
    "Real Estate Analyst": np.array([4, 4, 4, 4, 4, 4, 3, 4, 3, 4, 4, 5, 4, 4, 3, 3, 4, 4, 4, 4]),
    "Business Analyst": np.array([4, 4, 4, 5, 4, 5, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5]),
    "Management Consultant": np.array([5, 4, 5, 5, 4, 5, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5]),
    "Operations Research Analyst": np.array([4, 4, 4, 4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 5]),
    "Risk Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 5, 5, 4, 4, 4, 5, 4, 5, 4, 5, 4, 4]),
    "Investment Banking Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 5, 5, 5, 4, 4, 5, 4, 4, 5, 4, 5, 5]),
    "Wealth Management Advisor": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 4, 4, 4, 5, 4, 4, 5, 4, 5, 4]),
    "Asset Manager": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 4, 4, 4, 5, 4, 4, 5, 4, 5, 5]),
    "Research Economist": np.array([4, 4, 4, 3, 4, 5, 3, 4, 4, 4, 5, 5, 5, 4, 5, 4, 4, 5, 4, 5]),
},
"ecacc": {
    "Certified Public Accountant (CPA)": np.array([4, 3, 4, 3, 5, 3, 4, 3, 5, 4, 5, 5, 4, 4, 5, 5, 4, 3, 3, 4]),
    "Auditor": np.array([3, 4, 4, 3, 5, 3, 4, 3, 4, 4, 4, 5, 4, 4, 5, 5, 4, 3, 3, 4]),
    "Tax Accountant": np.array([4, 3, 3, 3, 5, 3, 4, 3, 4, 4, 4, 5, 3, 4, 5, 5, 4, 3, 4, 4]),
    "Financial Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 5, 4, 4, 4, 3, 3, 4, 5, 4, 5]),
    "Management Accountant (CMA)": np.array([4, 3, 4, 4, 5, 3, 3, 4, 4, 4, 5, 5, 4, 4, 5, 4, 5, 4, 5, 4]),
    "Forensic Accountant": np.array([4, 3, 3, 3, 5, 3, 4, 3, 4, 4, 4, 5, 4, 4, 5, 5, 4, 3, 4, 4]),
    "Budget Analyst": np.array([4, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 5, 4, 4, 3, 4, 4, 4, 4]),
    "Internal Auditor": np.array([3, 4, 4, 3, 5, 3, 4, 3, 4, 4, 4, 5, 4, 4, 5, 5, 4, 3, 3, 4]),
    "Cost Accountant": np.array([4, 3, 4, 4, 5, 3, 4, 3, 4, 4, 5, 4, 5, 4, 4, 4, 5, 4, 4, 4]),
    "Financial Controller": np.array([5, 3, 4, 4, 5, 4, 4, 4, 4, 5, 5, 4, 5, 4, 4, 4, 5, 5, 4, 5]),
    "Tax Consultant": np.array([4, 3, 3, 3, 5, 3, 4, 3, 4, 4, 4, 5, 3, 4, 5, 5, 4, 3, 4, 4]),
    "Corporate Treasurer": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 5, 4, 4, 4, 3, 3, 4, 5, 4, 5]),
    "Risk Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 5, 4, 4, 5, 3, 4, 4, 5, 4, 5]),
    "Investment Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 5, 4, 4, 4, 3, 4, 4, 5, 4, 5]),
    "Accounting Information Systems Specialist": np.array([4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 5, 5, 5, 4, 4, 4]),
},
"sds": {
    "Data Scientist": np.array([5, 3, 4, 4, 3, 5, 4, 4, 5, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5]),
    "Statistician": np.array([4, 4, 4, 4, 4, 4, 3, 4, 5, 4, 5, 4, 5, 4, 4, 4, 5, 3, 5, 4]),
    "Data Analyst": np.array([4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 5, 4, 5, 4, 3, 4, 4, 4, 4, 4]),
    "Financial Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 4, 5, 5, 4, 4, 4, 3, 4, 4, 4, 5, 4]),
    "Risk Analyst": np.array([5, 3, 4, 4, 4, 4, 3, 4, 5, 5, 4, 4, 4, 4, 4, 4, 5, 4, 5, 4]),
    "Actuary": np.array([5, 3, 3, 3, 4, 4, 3, 3, 5, 5, 5, 4, 5, 4, 4, 4, 5, 4, 5, 5]),
    "Machine Learning Engineer": np.array([4, 3, 3, 4, 3, 5, 4, 4, 5, 5, 5, 5, 5, 5, 5, 3, 4, 5, 4, 5]),
    "Data Engineer": np.array([4, 3, 3, 4, 3, 5, 4, 4, 4, 4, 5, 5, 4, 4, 5, 3, 4, 5, 4, 4]),
    "Business Intelligence Analyst": np.array([4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 5, 4, 5, 4, 3, 5, 4, 4, 4, 4]),
    "Operations Research Analyst": np.array([4, 4, 4, 4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5, 5]),
    "Marketing Analyst": np.array([4, 4, 5, 4, 4, 4, 3, 4, 4, 4, 4, 4, 5, 4, 3, 5, 4, 4, 3, 4]),
    "Data Visualization Specialist": np.array([4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 5, 4, 5, 4, 3, 5, 4, 4, 4, 4]),
    "Cloud Engineer": np.array([4, 3, 4, 4, 3, 5, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 3, 5, 4, 4]),
    "Artificial Intelligence Specialist": np.array([4, 3, 3, 4, 3, 5, 4, 4, 5, 5, 5, 5, 5, 5, 5, 3, 4, 5, 4, 5]),
    "Software Engineer (Data-Focused)": np.array([4, 3, 4, 4, 3, 5, 4, 4, 5, 5, 4, 4, 4, 4, 5, 4, 3, 5, 4, 4]),
},
}

    if major not in career_scores:
        raise ValueError(f"Major not found in career scores")
    
    major_scores = career_scores[major]
    weighted_scores = {}

    for career, career_vector in major_scores.items():
        similarity = cosine_similarity(student, career_vector)

        weighted_similarity = 1 * similarity
        weighted_scores[career] = weighted_similarity

    weighted_scores = normalize_scores(weighted_scores)
    weighted_scores = sorted(weighted_scores.items(), key=lambda x : x[1], reverse=True)

    top_5_careers = weighted_scores[:5]
    for career, score in top_5_careers:
        print(f"{career}: {score}")
    return top_5_careers

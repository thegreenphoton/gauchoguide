import numpy as np 
from scipy.spatial.distance import cosine
from numpy import dot
from numpy.linalg import norm
from collect_data import get_career_ratings


career_scores = {
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

}

example_student = np.array([4, 3, 5, 4, 4, 4, 3, 2, 1, 5, 4, 3, 4, 5, 3, 4, 2, 4, 5, 3])
example_student2 = np.array([5, 4, 4, 4, 3, 5, 4, 4, 4, 4, 4, 3, 1, 5, 4, 2, 3, 5, 4, 2])
example_student3 = np.array([2, 3, 4, 4, 4, 4, 4, 3, 4, 3, 2, 3, 2, 5, 3, 5, 2, 5, 3, 1])

def normalize_scores(scores):
    min_score = min(scores.values())
    max_score = max(scores.values())
    return {career: (score - min_score) / (max_score - min_score) for career, score in scores.items()}

def cosine_similarity(student, career):
    return dot(student, career) / (norm(student) * norm(career))

def calculate_weighted_similarity(student, career_scores):
    career_ratings = get_career_ratings()
    weighted_scores = {}
    for career, career_vector in career_scores.items():
        similarity = cosine_similarity(student, career_vector)
        weight = career_ratings.get(career, 1)
        weighted_similarity = weight * similarity
        weighted_scores[career] = weighted_similarity

    weighted_scores = normalize_scores(weighted_scores)
    weighted_scores = sorted(weighted_scores.items(), key=lambda x : x[1], reverse=True)

    top_5_careers = weighted_scores[:5]
    for career, score in top_5_careers:
        print(f"{career}: {score}")
    return top_5_careers

# calculate_weighted_similarity(example_student3, career_scores)




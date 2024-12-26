import pandas as pd
import os
from career_rec import calculate_weighted_similarity, example_student3, career_scores
import numpy as np

folder_path = 'data'
courses_file = os.path.join(folder_path, 'course_info.csv')
ce_relevancy_file = os.path.join(folder_path, 'ce_rel_vecs.csv')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

courses_df = pd.read_csv(courses_file)
relevance_df = pd.read_csv(ce_relevancy_file)

df = pd.merge(courses_df, relevance_df, on='Course', how='inner')

sequences = {
    "Computer Networks Sequence": ["CS 176A - Intro to Computer Communication Networks", "CS 176B - Network Computing"],
    "Computer Systems Design Sequence": ["ECE 153A - Hardware/Software Interface", "ECE 153B - Sensor and Peripheral Interface Design"],
    "Design and Test Automation Sequence": ["ECE 157A - Machine Learning in Design and Test Automation", "ECE 157B - Artificial Intelligence in Design and Test Automation"],
    "Distributed Systems Sequence": ["CS 171 - Distributed Systems", "CS 176A - Intro to Computer Communication Networks"],
    "Machine Learning Sequence": ["CS 165A - Artificial Intelligence", "CS 165B - Machine Learning"],
    "Multimedia Sequence": ["ECE 178 - Intro to Digital Image and Video Processing", "ECE 181 - Intro to Computer Vision"],
    "Programming Languages Sequence": ["CS 160 - Translation of Programming Languages", "CS 162 - Programming Languages"],
    "Real-Time Computing and Control Sequence": ["ECE 147A - Feedback Control Systems - Theory and Design", "ECE 147B - Digital Control Systems - Theory and Design"],
    "Robotics Sequence": ["ECE 179D - Intro to Robotics - Dynamics and Control", "ECE 179P - Intro to Robotics - Planning and Kinematics"],
    "Signals and Systems Sequence": ["ECE 130A - Signal Analysis and Processing I", "ECE 130B - Signal Analysis and Processing II"],
    "System Software Architecture Sequence": ["CS 170 - Operating Systems", "CS 171 - Distributed Systems"],
    "VLSI Sequence": ["ECE 122A - VLSI Principles I", "ECE 122B - VLSI Principles II"]
}

example_student = np.array([], dtype=float)
while len(example_student) < 20:
    try:
        num = float(input("Enter a number between 1-5: "))
        if 1<= num <= 5:
            example_student = np.append(example_student, num)
        else:
            print("invalid number")
    except ValueError:
        print("Invalid input")
# RANK SEQUENCES, THEN LET THE USER CHOOSE FROM REMAINING INDIVIDUAL COURSES

example_top_five = {
    "Software Engineer": 0.3,
    "Machine Learning Engineer": 0.3,
    "Hardware Engineer": 0.15,
    "Data Engineer": 0.15,
    "Cybersecurity Engineer": 0.1
}

top_careers = calculate_weighted_similarity(example_student, career_scores)
career_weights = {career: weight for career, weight in zip([c[0] for c in top_careers], [0.3, 0.3, 0.15, 0.15, 0.1])}

df['Weighted_Relevance'] = sum(df[career] * weight for career, weight in career_weights.items())

sequence_relevance = {}
for sequence, courses in sequences.items():
    relevant_courses = df[df['Course'].isin(courses)]
    averaged_relevance = relevant_courses['Weighted_Relevance'].mean()
    sequence_relevance[sequence] = averaged_relevance

sequences_df = pd.DataFrame(sequence_relevance.items(), columns=['Sequence', 'Weighted_Relevance'])




ranked_sequences = sequences_df.sort_values(by='Weighted_Relevance', ascending=False)
min_score = ranked_sequences['Weighted_Relevance'].min()
max_score = ranked_sequences['Weighted_Relevance'].max()
ranked_sequences['Normalized_Relevance'] = (
    (ranked_sequences['Weighted_Relevance'] - min_score) / (max_score - min_score)
)

ranked_sequences['Rescaled_Relevance'] = ranked_sequences['Normalized_Relevance'] * 100
ranked_sequences['Rescaled_Relevance'].fillna(0)

print(ranked_sequences[['Sequence', 'Rescaled_Relevance']])

chosen_sequences = []
while len(chosen_sequences) < 2:
    choice = input(f"Choose sequence {len(chosen_sequences) + 1}: ")
    if choice in sequences_df['Sequence'].values and choice not in chosen_sequences:
        chosen_sequences.append(choice)
    else:
        print("Invalid or duplicate choice. Try again.")
print("Chosen Sequences:")
for seq in chosen_sequences:
    print(seq)

chosen_courses = [course for seq in chosen_sequences for course in sequences[seq]]

standalone_electives1 = df[~df['Course'].isin(chosen_courses)]
standalone_electives = standalone_electives1[standalone_electives1['CE_Elective'] == 1]
ranked_standalone_electives = standalone_electives.sort_values(by='Weighted_Relevance', ascending=False)

min_score = ranked_standalone_electives['Weighted_Relevance'].min()
max_score = ranked_standalone_electives['Weighted_Relevance'].max()

ranked_standalone_electives['Normalized_Relevance'] = (
    (ranked_standalone_electives['Weighted_Relevance'] - min_score) / (max_score - min_score)
)

ranked_standalone_electives['Rescaled_Relevance'] = ranked_standalone_electives['Normalized_Relevance'] * 100

print(ranked_standalone_electives[['Course', 'Rescaled_Relevance']])

top_two_sequences = ranked_sequences.head(2)
selected_sequences = top_two_sequences["Sequence"].tolist()
top_two_sequence_courses = pd.DataFrame([
    {"Sequence": seq, "Course": course}
    for seq in selected_sequences
    for course in sequences[seq]
])
top_six_electives = ranked_standalone_electives.head(6)








electives = df[df['CE_Elective'] == 1]

ranked_electives = electives.sort_values(by='Weighted_Relevance', ascending=False)

min_score = ranked_electives['Weighted_Relevance'].min()
max_score = ranked_electives['Weighted_Relevance'].max()

ranked_electives['Normalized_Relevance'] = (
    (ranked_electives['Weighted_Relevance'] - min_score) / (max_score - min_score)
)

ranked_electives['Rescaled_Relevance'] = ranked_electives['Normalized_Relevance'] * 100



# print("Top Electives Based on Example Careers:")
# print(ranked_electives[['Course', 'Rescaled_Relevance']])
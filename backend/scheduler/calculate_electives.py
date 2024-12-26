import pandas as pd
import os
from .career_rec import calculate_weighted_similarity, career_scores
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def calculate_top_careers(example_student, career_scores):
    # Calculate similarity scores
    top_careers = calculate_weighted_similarity(example_student, career_scores)

    # Predefined weights
    weights = [0.5, 0.2, 0.10, 0.10, 0.1]

    # Combine relevance and weights
    top_careers_with_weights = [
        {"career": career, "relevance": round(score * 100, 2), "weight": weights[i]}
        for i, (career, score) in enumerate(top_careers[:5])
    ]

    return top_careers_with_weights

def calculate_top_electives(
        top_careers, career_scores
):
    folder_path = os.path.join(os.path.dirname(__file__), 'data')
    courses_file = os.path.join(folder_path, 'course_info.csv')
    ce_relevancy_file = os.path.join(folder_path, 'ce_rel_vecs.csv')



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

    # Validate top_careers format
    if not isinstance(top_careers, list) or not all(isinstance(career, dict) for career in top_careers):
        raise ValueError("Invalid format for top_careers. Expected a list of dictionaries.")

    # Extract weights and relevance
    career_weights = {career["career"]: career["weight"] for career in top_careers}

    # Ensure career names are strings and exist in DataFrame columns
    career_weights = {str(career): weight for career, weight in career_weights.items() if str(career) in df.columns}

    # Calculate weighted relevance safely
    df['Weighted_Relevance'] = sum(
        df[career] * weight for career, weight in career_weights.items()
    )
    sequence_relevance = {}
    for sequence, courses in sequences.items():
        relevant_courses = df[df['Course'].isin(courses)]
        averaged_relevance = relevant_courses['Weighted_Relevance'].mean()
        sequence_relevance[sequence] = averaged_relevance

    incompatible_sequence_pairs = {
        ("Computer Networks Sequence", "Distributed Systems Sequence"),
        ("Distributed Systems Sequence", "System Software Architecture Sequence")
    }

    sequences_df = pd.DataFrame(sequence_relevance.items(), columns=['Sequence', 'Weighted_Relevance'])
    ranked_sequences = sequences_df.sort_values(by='Weighted_Relevance', ascending=False)

    min_score = ranked_sequences['Weighted_Relevance'].min()
    max_score = ranked_sequences['Weighted_Relevance'].max()
    ranked_sequences['Normalized_Relevance'] = (
        (ranked_sequences['Weighted_Relevance'] - min_score) / (max_score - min_score)
    )

    ranked_sequences['Rescaled_Relevance'] = ranked_sequences['Normalized_Relevance'] * 100
    ranked_sequences['Rescaled_Relevance'].fillna(0)

    selected_sequences = []
    i = 0

    #top_two_sequences = ranked_sequences.iloc[0:2]
    #selected_sequences = top_two_sequences["Sequence"].tolist()
    while len(selected_sequences) < 2 and i < len(ranked_sequences):
        seq = ranked_sequences.iloc[i]['Sequence']

        # Check for incompatibility with already selected sequences
        if any((seq, s) in incompatible_sequence_pairs or (s, seq) in incompatible_sequence_pairs for s in selected_sequences):
            print(f"Skipping incompatible pair: {selected_sequences[0]} and {seq}")
            i += 1
            continue  # Skip this sequence

        # Add the sequence if it's valid
        selected_sequences.append(seq)
        i += 1
        
    top_two_sequences = pd.DataFrame({"Sequence": selected_sequences})
    top_two_sequence_courses = pd.DataFrame([
        {"Sequence": seq, "Course": course}
        for seq in selected_sequences
        for course in sequences.get(seq, [])
    ])

    print(top_two_sequences[['Sequence']])

    top_two_sequence_course_list = top_two_sequence_courses['Course'].tolist()
    print(top_two_sequence_course_list)
    standalone_electives = df[
        (~df['Course'].isin(top_two_sequence_course_list)) & 
        (df['CE_Elective'].fillna(0) == 1)
    ]   
    #standalone_electives1 = df[~df['Course'].isin(top_two_sequence_courses)]
   # standalone_electives = standalone_electives1[standalone_electives1['CE_Elective'] == 1]
    ranked_standalone_electives = standalone_electives.sort_values(by='Weighted_Relevance', ascending=False)

    min_score = ranked_standalone_electives['Weighted_Relevance'].min()
    max_score = ranked_standalone_electives['Weighted_Relevance'].max()

    ranked_standalone_electives['Normalized_Relevance'] = (
        (ranked_standalone_electives['Weighted_Relevance'] - min_score) / (max_score - min_score)
    )

    ranked_standalone_electives['Rescaled_Relevance'] = ranked_standalone_electives['Normalized_Relevance'] * 100

    print(ranked_standalone_electives[['Course', 'Rescaled_Relevance']])

    top_six_electives = ranked_standalone_electives.head(6)

    return top_two_sequences, top_two_sequence_courses, top_six_electives, df


example_student = np.array([4, 5, 4, 3, 4, 5, 5, 4, 3, 4, 2, 5, 4, 5, 5, 3, 5, 4, 5, 2], dtype=float)




#calculate_top_electives(example_student, career_scores)
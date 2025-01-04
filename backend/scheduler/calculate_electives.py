import pandas as pd
import os
from .career_rec import calculate_weighted_similarity
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def get_major_dataframe(major):
    folder_path = os.path.join(os.path.dirname(__file__), 'data', major)
    courses_file = os.path.join(folder_path, 'course_info.csv')
    relevancy_file = os.path.join(folder_path, 'rel_vecs.csv')
    prereqs_file = os.path.join(folder_path, 'course_prereqs.csv')
    try: 
       
        courses_df = pd.read_csv(courses_file)
        relevance_df = pd.read_csv(relevancy_file)
        prereqs_df = pd.read_csv(prereqs_file)

        merged_df = pd.merge(courses_df, relevance_df, on='Course', how='inner')
        merged_df = pd.merge(merged_df, prereqs_df, on='Course', how='left')
        
        return merged_df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {str(e)}")
    except pd.errors.EmptyDataError as e:
        raise Exception(f"Empty CSV file: {str(e)}")
    except pd.errors.ParserError as e:
        raise Exception(f"Error parsing CSV file: {str(e)}")
    except KeyError as e:
        raise KeyError(f"Merge error: 'Course' column not found in one of the CSV files: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
    
def calculate_top_careers(example_student, major):

    top_careers = calculate_weighted_similarity(example_student, major)

    # Predefined weights
    weights = [0.5, 0.2, 0.10, 0.10, 0.1]
    top_careers_with_weights = [
        {"career": career, "relevance": round(score * 100, 2), "weight": weights[i]}
        for i, (career, score) in enumerate(top_careers[:5])
    ]

    return top_careers_with_weights

def calculate_top_electives(top_careers, major):
  
    df = get_major_dataframe(major)
    included_courses = set()

    if 'Prerequisites' in df.columns:
        prerequisites_map = {
            row['Course']: [p.strip() for p in row['Prerequisites'].split(',')] 
            if pd.notna(row['Prerequisites']) else []
            for _, row in df.iterrows()
        }
    required_courses = set(df[df['Required'] == 1]['Course'].values)

    ce_sequences = {
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
    requires_sequences = major == "ce"

    if not isinstance(top_careers, list) or not all(isinstance(career, dict) for career in top_careers):
        raise ValueError("Invalid format for top_careers. Expected a list of dictionaries.")

    career_weights = {career["career"]: career["weight"] for career in top_careers}
    career_weights = {str(career): weight for career, weight in career_weights.items() if str(career) in df.columns}

    df['Weighted_Relevance'] = sum(
        df[career] * weight for career, weight in career_weights.items()
    )
    if requires_sequences:
        sequence_relevance = {}
        for sequence, courses in ce_sequences.items():
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

        while len(selected_sequences) < 2 and i < len(ranked_sequences):
            seq = ranked_sequences.iloc[i]['Sequence']

            # Check for incompatibility with already selected sequences
            if any((seq, s) in incompatible_sequence_pairs or (s, seq) in incompatible_sequence_pairs for s in selected_sequences):
                print(f"Skipping incompatible pair: {selected_sequences[0]} and {seq}")
                i += 1
                continue 

            # Add the sequence if it's valid
            selected_sequences.append(seq)
            i += 1
            
        top_two_sequences = pd.DataFrame({"Sequence": selected_sequences})
        top_two_sequence_courses = pd.DataFrame([
            {"Sequence": seq, "Course": course}
            for seq in selected_sequences
            for course in ce_sequences.get(seq, [])
        ])

        print(top_two_sequences[['Sequence']])

        top_two_sequence_course_list = top_two_sequence_courses['Course'].tolist()
        print(top_two_sequence_course_list)
        electives = df[
            (~df['Course'].isin(top_two_sequence_course_list)) & 
            (df['Elective'].fillna(0) == 1)
        ]   

        electives = electives.sort_values(by='Weighted_Relevance', ascending=False)

        min_score = electives['Weighted_Relevance'].min()
        max_score = electives['Weighted_Relevance'].max()

        electives['Normalized_Relevance'] = (
            (electives['Weighted_Relevance'] - min_score) / (max_score - min_score)
        )

        electives['Rescaled_Relevance'] = electives['Normalized_Relevance'] * 100

        print(electives[['Course', 'Rescaled_Relevance']])

        top_six_electives = electives.head(6)
        top_six_electives = top_six_electives.fillna(0)
        top_two_sequences = top_two_sequences.fillna(0)
        top_two_sequence_courses = top_two_sequence_courses.fillna(0)
        return top_two_sequences, top_two_sequence_courses, top_six_electives
    
    elif major == "ecacc":
        area_e = df[df["Ecacc_E"] == 1].sort_values(by='Weighted_Relevance', ascending=False)
        area_i = df[df["Ecacc_I"] == 1].sort_values(by='Weighted_Relevance', ascending=False)
        electives1 = area_e.head(1)
        electives2 = area_i.head(2)
        electives = pd.concat([electives1, electives2], ignore_index=True)

    elif major == "sds":
        reg = df[df['Elective'] == 1].sort_values(by='Weighted_Relevance', ascending=False)
        math = df[df['Sds_math'] == 1].sort_values(by='Weighted_Relevance', ascending=False)
        reg_electives = reg.head(6)
        math_electives = math.head(2)
        electives = pd.concat([reg_electives, math_electives], ignore_index=True)
        
    else:
        electives = df[df['Elective'] == 1].sort_values(by='Weighted_Relevance', ascending=False)

    min_score = electives['Weighted_Relevance'].min()
    max_score = electives['Weighted_Relevance'].max()
    electives['Normalized_Relevance'] = (
        (electives['Weighted_Relevance'] - min_score) / (max_score - min_score)
    )

    electives['Rescaled_Relevance'] = electives['Normalized_Relevance'] * 100
    electives['Rescaled_Relevance'].fillna(0)
    electives = electives.fillna(0)

    num_electives = 6 if requires_sequences else (14 if major == "compsci" else 9 if major == "ee" else 7)
    selected_electives = []

    if major != "sds":
        for _, row in electives.iterrows():
            course = row['Course']
            prerequisites = prerequisites_map.get(course, [])

            unsatisfied_prereqs = [p for p in prerequisites if p not in included_courses]

            for prereq in unsatisfied_prereqs:

                # Check if the prerequisite is already included
                if prereq in included_courses or prereq in required_courses:
                    continue

                prereq_row = df[df['Course'] == prereq]

                if prereq_row.empty:
                    print(f"Prerequisite {prereq} not found in the dataset!")
                    continue  

                    # Extract the row safely
                prereq_row = prereq_row.iloc[0]

                    # Handle case when we need to replace a low-relevance elective
                if len(selected_electives) >= num_electives:
                        # Find the lowest-scoring elective
                    lowest_elective = min(selected_electives, key=lambda x: x['Weighted_Relevance'])

                        # Replace the lowest elective if it has lower relevance
                    if lowest_elective['Weighted_Relevance'] < row['Weighted_Relevance']:
                        print(f"Replacing {lowest_elective['Course']} with prerequisite {prereq}")
                        selected_electives.remove(lowest_elective)
                        selected_electives.append(prereq_row.to_dict())
                        included_courses.add(prereq)
                else:
                        # If there is space, add the prerequisite directly
                    selected_electives.append(prereq_row.to_dict())
                    included_courses.add(prereq)

            if len(selected_electives) < num_electives:
                selected_electives.append(row.to_dict())
                included_courses.add(course)

        selected_course_names = [elective['Course'] for elective in selected_electives]
        electives = electives[electives['Course'].isin(selected_course_names)].copy()
        electives = electives.sort_values(by='Weighted_Relevance', ascending=False)

    if major == "compsci":
        electives = electives.head(14)
        print(electives[['Course', 'Rescaled_Relevance']])
    elif major == "ee":
        electives = electives.head(9)
        print(electives[['Course', 'Rescaled_Relevance']])
    elif major == "econ":
        electives = electives.head(7)
        print(electives[['Course', 'Rescaled_Relevance']])

    return [], [], electives
        
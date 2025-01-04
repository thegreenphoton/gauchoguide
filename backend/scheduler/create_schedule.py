import pandas as pd
from collections import defaultdict, deque
import os

def map_difficulties(terms, difficulties_df):
    course_difficulties = []
    for term_index, term in enumerate(terms):
        term_details = []
        for course in term:
            if "G.E." in course:
                difficulty = 3.0
            else:
                difficulty_row = difficulties_df[difficulties_df['Course'] == course]
                if not difficulty_row.empty:
                    difficulty = difficulty_row['Final_Difficulty_Score'].values[0]
                else:
                    difficulty = 3.0
            term_details.append({"course": course, "difficulty": round(difficulty, 1)})

        course_difficulties.append({"term": term_index + 1, "courses": term_details})

    return course_difficulties

def course_scheduler(prerequisites, final_courses, prereqs_df, difficulties_df, major): 
    term_length = None
    if major == "ce" or major == "ee":
        term_length = 4
    elif major == "ecacc":
        term_length = 2
    else:
        term_length = 3
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for course, prereqs in prerequisites.items():
        for prereq in prereqs:
            graph[prereq].append(course)
            in_degree[course] += 1

    queue = deque([course for course in final_courses if in_degree[course] == 0])
    schedule = []
    term_mapping = {0: 'Offered_Fall', 1: 'Offered_Winter', 2: 'Offered_Spring'}
    terms = []
    term_difficulties = []
    current_term = 0
    deferred_courses = defaultdict(list)

    def find_next_available_term(course, current_term):

        offered_terms = [
            term for term, col in term_mapping.items()
            if prereqs_df.loc[prereqs_df['Course'] == course, col].values[0] == 1
        ]
        for term_offset in range(1, 10):  # Check up to the next 10 terms
            next_term = (current_term + term_offset) % 3  # Rotate through terms
            if next_term in offered_terms:
                return next_term
        return None  # No available term found

    while queue:
        term = []
        next_queue = deque()

        while queue and len(term) < term_length:
            course = queue.popleft()

            # Check if the course is offered in the current term
            if course in prereqs_df['Course'].values:
                offered_in_current_term = prereqs_df.loc[prereqs_df['Course'] == course, term_mapping[current_term]].fillna(0).values
                if len(offered_in_current_term) > 0 and offered_in_current_term[0] == 1:
                    # Check if prerequisites are met
                    unmet_prereqs = [prereq for prereq in prerequisites[course] if prereq not in schedule]
                    if not unmet_prereqs:
                        term.append(course)
                        schedule.append(course)
                    else:
                        print(f"Course {course} deferred due to unmet prerequisites: {unmet_prereqs}")
                        next_queue.append(course)  # Defer due to unmet prerequisites
                else:
                    # Defer to the next available term
                    next_available_term = find_next_available_term(course, current_term)
                    if next_available_term is not None:
                        deferred_courses[next_available_term].append(course)
                    else:
                        print(f"Course {course} could not be scheduled as it is not offered in any future terms.")
            else:
                print(f"Course {course} not found in offerings; deferred.")
                next_queue.append(course)

        if term:
            terms.append(term)

            term_courses_df = difficulties_df[difficulties_df['Course'].isin(term)]
            term_difficulty = term_courses_df['Final_Difficulty_Score'].sum()
            term_difficulties.append(term_difficulty.round(1))

            # Update in-degree for the next iteration
        for completed_course in term:
            for neighbor in graph[completed_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_queue.append(neighbor)

        # Requeue deferred courses for the next term
        current_term = (current_term + 1) % 3
        
        for course in deferred_courses[current_term]:
            offered_in_term = prereqs_df.loc[
                prereqs_df['Course'] == course, term_mapping[current_term]
            ].values[0]
            if offered_in_term == 1 and course not in schedule:
                queue.append(course)
            else:
                next_available_term = find_next_available_term(course, current_term)
                if next_available_term == None:
                    deferred_courses[next_available_term].append(course)

        deferred_courses[current_term] = []  # Clear deferred courses for the processed term
        queue.extend(next_queue)

    free_electives = ["G.E. 1", "G.E. 2", "G.E. 3",
                      "G.E. 4", "G.E. 5", "G.E. 6", 
                      "G.E. 7", "G.E. 8", "G.E. 9",
                      "G.E. 10", "G.E. 11", "G.E. 12"] 
    elective_index = 0  # To keep track of added electives

    # Add electives until the term has 3 courses for full time standing
    for term in terms:
        while len(term) < 3 and elective_index < len(free_electives):  
            term.append(free_electives[elective_index])
            elective_index += 1

    print("Course Schedule by Terms:")
    for i, term in enumerate(terms):        
        print(f"Term {i + 1}, difficulty = {term_difficulties[i]}: {', '.join(term)}")


    return terms, term_difficulties

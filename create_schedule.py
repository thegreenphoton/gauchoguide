import pandas as pd
from collections import defaultdict, deque
from calculate_electives import top_two_sequence_courses, top_six_electives, chosen_courses, df
from difficulty_pred import difficulties_df
import os

folder_path = 'data'

prereqs_file = os.path.join(folder_path, 'course_prereqs.csv')
offering_schedule_file = os.path.join(folder_path, 'course_offerings.csv')
capstone_file = os.path.join(folder_path, 'capstone_flags.csv')

prereqs_df_initial  = pd.read_csv(prereqs_file)
offering_schedule = pd.read_csv(offering_schedule_file)

prereqs_df = pd.merge(prereqs_df_initial, offering_schedule, on='Course', how='left')

required_courses = df[df['CE_required'] == 1]
capstone_df = pd.read_csv(capstone_file)
capstone_courses = capstone_df[capstone_df['CE_capstone'] == 1]

capstone_groups = {
    "CS Capstone": capstone_courses[capstone_courses['Course'].str.contains('CS')]['Course'].tolist(),
    "CE Capstone": capstone_courses[capstone_courses['Course'].str.contains('CE')]['Course'].tolist()
}

print("Choose your capstone:")
for i, (capstone_name, courses) in enumerate(capstone_groups.items(), 1):
    print(f"{i}. {capstone_name}: {','.join(courses)}")
choice_index = int(input("Enter the number of your choice: ")) - 1
chosen_capstone_name = list(capstone_groups.keys())[choice_index]
chosen_capstone_courses = capstone_groups[chosen_capstone_name]

final_courses = pd.concat([
    #top_two_sequence_courses[["Course"]],
    pd.DataFrame({"Course": chosen_courses}),
    top_six_electives[["Course"]],
    required_courses[["Course"]],
    pd.DataFrame({"Course": chosen_capstone_courses})
    
]).drop_duplicates().reset_index(drop=True)

print(final_courses)

final_courses = final_courses['Course'].tolist()

filtered_prereq_df = prereqs_df[prereqs_df['Course'].isin(final_courses)].copy()
filtered_prereq_df['Prerequisites'] = filtered_prereq_df['Prerequisites'].apply(
    lambda prereqs: ','.join([prereq for prereq in (prereqs.split(',') if pd.notna(prereqs) else []) if prereq in final_courses])
)


prerequisites = filtered_prereq_df.set_index('Course')['Prerequisites'].apply(
    lambda x: x.split(',') if pd.notna(x) and x else []
).to_dict()

graph = defaultdict(list)
in_degree = defaultdict(int)

for course, prereqs in prerequisites.items():
    for prereq in prereqs:
        graph[prereq].append(course)
        in_degree[course] += 1

queue = deque([course for course in final_courses if in_degree[course] == 0])
schedule = []

# Step 3: Assign courses to terms
term_mapping = {0: 'Offered_Fall', 1: 'Offered_Winter', 2: 'Offered_Spring'}
terms = []
term_difficulties = []
current_term = 0
deferred_courses = defaultdict(list)  # Track deferred courses by term

def find_next_available_term(course, current_term):

    offered_terms = [
        term for term, col in term_mapping.items()
        if prereqs_df.loc[prereqs_df['Course'] == course, col].values[0] == 1
    ]
    for term_offset in range(1, 10):  # Check up to the next 3 terms
        next_term = (current_term + term_offset) % 3  # Rotate through terms
        # term_column = term_mapping[next_term]
        if next_term in offered_terms:
            return next_term
    return None  # No available term found

while queue:
    term = []
    next_queue = deque()

    while queue and len(term) < 4:
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
        term_difficulties.append(term_difficulty.round(2))

       # print(f"Term {len(terms)} difficulty: {term_difficulty}")

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
        if offered_in_term == 1:
            queue.append(course)
        else:
            next_available_term = find_next_available_term(course, current_term)
            if next_available_term == None:
                deferred_courses[next_available_term].append(course)

    deferred_courses[current_term] = []  # Clear deferred courses for the processed term
    queue.extend(next_queue)

print("Course Schedule by Terms:")
for i, term in enumerate(terms):
    print(f"Term {i + 1}, difficulty = {term_difficulties[i]}: {', '.join(term)}")

for capstone in chosen_capstone_courses:
    if capstone not in schedule:
        print(f"Error: Capstone course {capstone} was not scheduled.")
        exit()


# Validate if all courses are scheduled
if len(schedule) != len(final_courses):
    print("Error: Some courses could not be scheduled due to cyclic dependencies or unmet prerequisites.")

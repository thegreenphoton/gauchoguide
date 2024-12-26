import pandas as pd
import os

def course_difficulty_predictor():
    folder_path = os.path.join(os.path.dirname(__file__), 'data')
    courses_file = os.path.join(folder_path, 'course_info.csv')
    relevancy_file = os.path.join(folder_path, 'ce_rel_vecs.csv')

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    courses_df = pd.read_csv(courses_file)
    relevance_df = pd.read_csv(relevancy_file)

    difficulties_df = pd.merge(courses_df, relevance_df, on='Course', how='inner')

    #calculates total num of students
    difficulties_df['Total_Students'] = difficulties_df[['A_Count', 'B_Count', 'C_Count', 'D_Count', 'F_Count']].sum(axis=1) 

    difficulties_df['Avg_Grade'] = (
        (4 * difficulties_df['A_Count'] + 3 * difficulties_df['B_Count'] + 2 * difficulties_df['C_Count'] + 1 * difficulties_df['D_Count'] + 0 * difficulties_df['F_Count'])
        / difficulties_df['Total_Students']
    )

    #normalize avg grade
    difficulties_df['Avg_Grade_Normalized'] = 1 - (difficulties_df['Avg_Grade'] / 4)

    difficulties_df['Failure_Rate'] = (difficulties_df['D_Count'] + difficulties_df['F_Count']) / difficulties_df['Total_Students']
    difficulties_df['Failure_Rate_Normalized'] = difficulties_df['Failure_Rate'] / difficulties_df['Failure_Rate'].max()

    difficulties_df['Grade_Distribution'] = difficulties_df[['A_Count', 'B_Count', 'C_Count', 'D_Count', 'F_Count']].std(axis=1)
    difficulties_df['Variability_Normalized'] = difficulties_df['Grade_Distribution'] / difficulties_df['Grade_Distribution'].max()

    difficulties_df['Conceptual_Rating_Normalized'] = difficulties_df['GPT_concept_rating'] / 10

    field_multipliers = {
        "Engineering": 1.1,
        "CS": 1.1,
        "Economics": 1.0,
        "Communication": 0.9,
        "History": 0.9
    }

    difficulties_df['Multiplier'] = difficulties_df['Field'].map(field_multipliers)

    difficulties_df['Difficulty_Score'] = (
        0.25 * difficulties_df['Avg_Grade_Normalized'] +
        0.20 * difficulties_df['Failure_Rate_Normalized'] +
        0.05 * difficulties_df['Variability_Normalized'] +
        0.35 * difficulties_df['Conceptual_Rating_Normalized']
    ) * 10

    difficulties_df['Field_Adjusted_Difficulty_Score'] = difficulties_df['Difficulty_Score'] * difficulties_df['Multiplier']

    max_score = difficulties_df['Field_Adjusted_Difficulty_Score'].max()
    min_score = difficulties_df['Field_Adjusted_Difficulty_Score'].min()

    difficulties_df['Final_Difficulty_Score'] = (
        9 * (difficulties_df['Field_Adjusted_Difficulty_Score'] - min_score) / (max_score - min_score) + 1
    ).round(2)

    difficulties_df.to_csv('courses_with_difficulty.csv', index=False)

    #print(difficulties_df[['Course', 'Final_Difficulty_Score']])

    return difficulties_df




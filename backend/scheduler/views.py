from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .create_schedule import course_scheduler, map_difficulties
from .calculate_electives import calculate_top_electives, calculate_top_careers, get_major_dataframe
from .difficulty_pred import course_difficulty_predictor
import numpy as np
import logging
import os
import pandas as pd
import gc

gc.collect()
logger = logging.getLogger(__name__)

class CareerRecommendationView(APIView):
    def post(self, request):
        try: 
            major = request.data.get('major')
            if not major:
                return Response({"error": "Major is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            example_student = request.data.get('exampleStudent', [])

            if len(example_student) != 20:
                return Response({"error": "invalid input format. must be length 20"}, status=status.HTTP_400_BAD_REQUEST)
            
            example_student = np.array(example_student, dtype=float)

            top_5_careers = calculate_top_careers(example_student, major)

            return Response({
                "exampleStudent": example_student.tolist(),
                "topCareers": top_5_careers
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseSchedulerView(APIView):
    def post(self, request):
        try:
            major = request.data.get('major')
            is_manual_route = request.data.get('manualRoute', False)

            if is_manual_route:
                selected_careers = request.data.get("selectedCareers", [])
                if not isinstance(selected_careers, list):
                    return Response({"error": "Invalid format for selectedCareers. Must be a list."}, status=status.HTTP_400_BAD_REQUEST)

                # Manual route: no exampleStudent needed
                top_careers = selected_careers

            else:
                # Survey route
                example_student = request.data.get("exampleStudent", [])
                if len(example_student) != 20:
                    return Response({"error": "Invalid input format. Must have 20 responses."}, status=status.HTTP_400_BAD_REQUEST)
                example_student = np.array(example_student, dtype=float)
                top_careers = calculate_top_careers(example_student, major)

            folder_path = os.path.join(os.path.dirname(__file__), 'data', major)
            prereqs_file = os.path.join(folder_path, 'course_prereqs.csv')
            offering_schedule_file = os.path.join(folder_path, 'course_offerings.csv')
            prereqs_df_initial = pd.read_csv(prereqs_file)
            offering_schedule = pd.read_csv(offering_schedule_file)
            prereqs_df = pd.merge(prereqs_df_initial, offering_schedule, on='Course', how='left')

            print(f"Major received: {major}")
            df = get_major_dataframe(major)
            required_courses = df[df['Required'] == 1]

            if major == "ce":

                top_two_sequences_raw = request.data.get("topTwoSequences", [])
                top_two_sequence_courses_raw = request.data.get("topSequenceCourses", [])
                top_six_electives_raw = request.data.get("topSixElectives", [])

                top_two_sequences = [seq['Sequence'] for seq in top_two_sequences_raw]
                top_two_sequence_courses = [course['Course'] for course in top_two_sequence_courses_raw]
                top_six_electives = [course['Course'] for course in top_six_electives_raw]

                capstone_file = os.path.join(folder_path, 'capstone_flags.csv')
                capstone_df = pd.read_csv(capstone_file)
                capstone_courses = capstone_df[capstone_df['CE_capstone'] == 1]

                capstone_groups = {
                    "CS Capstone": capstone_courses[capstone_courses['Course'].str.contains('CS')]['Course'].tolist(),
                    "CE Capstone": capstone_courses[capstone_courses['Course'].str.contains('CE')]['Course'].tolist()
                }

                chosen_capstone_courses = capstone_groups["CE Capstone"]

                final_courses = pd.concat([
                    pd.DataFrame({"Course": top_two_sequence_courses}),
                    pd.DataFrame({"Course": top_six_electives}),
                    required_courses[["Course"]],
                    pd.DataFrame({"Course": chosen_capstone_courses})
                ]).drop_duplicates().reset_index(drop=True)
                print(final_courses)
                final_courses = final_courses['Course'].unique().tolist()

            elif major == "ee":
                
                electives_raw = request.data.get("electives", [])

                electives = [course['Course'] for course in electives_raw]

                capstone_file = os.path.join(folder_path, 'capstone_flags.csv')
                capstone_df = pd.read_csv(capstone_file)
                capstone_courses = capstone_df[capstone_df['EE_capstone'] == 1]

                capstone_groups = {
                    "EE Capstone": capstone_courses[capstone_courses['Course'].str.contains('EE')]['Course'].tolist(),
                    "CE Capstone": capstone_courses[capstone_courses['Course'].str.contains('CE')]['Course'].tolist()
                }

                chosen_capstone_courses = capstone_groups["EE Capstone"]

                final_courses = pd.concat([
                    pd.DataFrame({"Course": electives}),
                    required_courses[["Course"]],
                    pd.DataFrame({"Course": chosen_capstone_courses})
                ]).drop_duplicates().reset_index(drop=True)
                print(final_courses)
                final_courses = final_courses['Course'].unique().tolist()
            elif major == "compsci":
                electives_raw = request.data.get("electives", [])

                electives = [course['Course'] for course in electives_raw]

                capstone_file = os.path.join(folder_path, 'capstone_flags.csv')
                capstone_df = pd.read_csv(capstone_file)
                capstone_courses = capstone_df[capstone_df['CS_capstone'] == 1]

                capstone_groups = {
                    "CS Capstone": capstone_courses[capstone_courses['Course'].str.contains('CS')]['Course'].tolist(),
                    "CE Capstone": capstone_courses[capstone_courses['Course'].str.contains('CE')]['Course'].tolist()
                }

                chosen_capstone_courses = capstone_groups["CS Capstone"]

                final_courses = pd.concat([
                    pd.DataFrame({"Course": electives}),
                    required_courses[["Course"]],
                    pd.DataFrame({"Course": chosen_capstone_courses})
                ]).drop_duplicates().reset_index(drop=True)
                print(final_courses)
                final_courses = final_courses['Course'].unique().tolist()
            else:
                electives_raw = request.data.get("electives", [])

                electives = [course['Course'] for course in electives_raw]
                final_courses = pd.concat([
                    pd.DataFrame({"Course": electives}),
                    required_courses[["Course"]]
                ]).drop_duplicates().reset_index(drop=True)
                print(final_courses)
                final_courses = final_courses['Course'].unique().tolist()



            filtered_prereq_df = prereqs_df[prereqs_df['Course'].isin(final_courses)].copy()
            filtered_prereq_df['Prerequisites'] = filtered_prereq_df['Prerequisites'].apply(
                lambda prereqs: ','.join(
                    [prereq for prereq in (prereqs.split(',') if pd.notna(prereqs) else []) if prereq in final_courses]
                )
            )

            prerequisites = filtered_prereq_df.set_index('Course')['Prerequisites'].apply(
                lambda x: x.split(',') if pd.notna(x) and x else []
            ).to_dict()

            # Calculate schedule
            difficulties_df = course_difficulty_predictor(major)
            terms, term_difficulties = course_scheduler(prerequisites, final_courses, prereqs_df, difficulties_df, major)
            course_difficulties = map_difficulties(terms, difficulties_df)
            # Prepare response
            schedule = []
            for i, term in enumerate(terms):
                schedule.append({
                    "term": i + 1,
                    "courses": course_difficulties[i]["courses"],
                    "difficulty": term_difficulties[i]
                })

            return Response({"schedule": schedule}, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.error(f"Schedule error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error calculating schedule: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ElectivesView(APIView):
    def post(self, request):
        try:
            # Check if manual route
            is_manual_route = request.data.get('manualRoute', False)
            major = request.data.get('major')

            if not major:
                return Response({"error": "major is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            if is_manual_route:
                # Process manually selected careers
                selected_careers = request.data.get("selectedCareers", [])

                # Validate structure of each career object
                if not isinstance(selected_careers, list) or len(selected_careers) != 5:
                    return Response(
                        {"error": "Invalid selectedCareers format or length."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Ensure each career has the required fields
                for career in selected_careers:
                    if not isinstance(career, dict) or not all(k in career for k in ["career", "relevance", "weight"]):
                        return Response(
                            {"error": f"Invalid career format: {career}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # Use the careers directly
                top_careers = selected_careers

            else:
                # Process survey route
                example_student = request.data.get("exampleStudent", [])
                if not isinstance(example_student, list) or len(example_student) != 20:
                    return Response(
                        {"error": "Invalid exampleStudent format."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                example_student = np.array(example_student, dtype=float)
                top_careers = calculate_top_careers(example_student, major)

            if major == "ce":
                top_two_sequences, top_two_sequence_courses, electives = calculate_top_electives(top_careers, major)
     
                return Response({
                    "topTwoSequences": top_two_sequences.to_dict(orient='records'),
                    "topSequenceCourses": top_two_sequence_courses.to_dict(orient='records'),
                    "topSixElectives": electives.to_dict(orient='records'),
                }, status=status.HTTP_200_OK)
            
            else:
                try:
                    electives = pd.DataFrame()
                    result = calculate_top_electives(top_careers, major)
                    _, _, electives = result
                except Exception as e:
                    logger.error(f"Error calculating electives for major {major}: {str(e)}")
                    return Response({"error": f"Failed to calculate electives for {major}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({
                    "electives": electives.to_dict(orient='records')
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing electives: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

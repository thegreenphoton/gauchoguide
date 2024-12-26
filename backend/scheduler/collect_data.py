import sqlite3

conn = sqlite3.connect("career_feedback.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
             user_id INTEGER,
             career TEXT,
             rating INTEGER
    ) 
""")
conn.commit()

def store_feedback(user_id, career, rating): ##store feedback from users that have chosen their career
    cursor.execute("INSERT INTO feedback (user_id, career, rating) VALUES (?, ?, ?)", (user_id, career, rating))
    conn.commit()

from django.db.models import Avg
from scheduler.models import Feedback  # Replace `your_app` and `Feedback` with actual app/model names

def get_career_ratings():
    return Feedback.objects.values('career').annotate(avg_rating=Avg('rating'))




    
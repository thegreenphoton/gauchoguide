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

def get_career_ratings(): ##get the average ratings, or weights, of the careers
    cursor.execute("SELECT career, AVG(rating) as avg_rating FROM feedback GROUP BY career")
    return dict(cursor.fetchall())



    
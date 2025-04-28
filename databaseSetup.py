import sqlite3

def create_tables():
    conn = sqlite3.connect('calorie_tracker.db')
    c = conn.cursor()
    
    # Drop the existing table if it exists (optional, for clean setup)
    c.execute('''DROP TABLE IF EXISTS user_data''')
    c.execute('''DROP TABLE IF EXISTS meals''')
    
    # Create user_data table with macronutrient columns
    c.execute('''CREATE TABLE IF NOT EXISTS user_data
                 (id INTEGER PRIMARY KEY, gender TEXT, age INTEGER, weight REAL, height REAL, activity_level INTEGER, 
                  total_calories REAL, total_proteins REAL, total_fats REAL, total_carbs REAL)''')
    
    # Create meals table with macronutrient columns
    c.execute('''CREATE TABLE IF NOT EXISTS meals
                 (id INTEGER PRIMARY KEY, user_id INTEGER, meal_name TEXT, calories REAL, proteins REAL, fats REAL, carbs REAL,
                  FOREIGN KEY(user_id) REFERENCES user_data(id))''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
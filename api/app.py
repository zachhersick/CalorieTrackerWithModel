from flask import Flask, request, jsonify
import sqlite3
from databaseSetup import create_tables
from CalorieTrackerGUI import getBMR, getCalories
from inference import predict_calories

app = Flask(__name__)
create_tables()  # ensure tables exist on cold start

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    method = data.get('method', 'bmi')
    if method == 'bmi':
        bmr = getBMR(
          data['gender'], data['age'],
          data['weight'], data['height']
        )
        calories = getCalories(bmr, data['activity'])
    else:
        calories = predict_calories(data)
    return jsonify({'calories': calories})

@app.route('/log_meal', methods=['POST'])
def log_meal():
    d = request.get_json()
    conn = sqlite3.connect('calorie_tracker.db')
    c = conn.cursor()
    c.execute("""
      INSERT INTO meals (user_id, meal_name, calories, proteins, fats, carbs)
      VALUES (?, ?, ?, ?, ?, ?)""",
      (d['user_id'], d['meal_name'],
       d['calories'], d['proteins'],
       d['fats'], d['carbs'])
    )
    conn.commit(); conn.close()
    return jsonify({'status': 'success'})

@app.route('/get_meals', methods=['GET'])
def get_meals():
    conn = sqlite3.connect('calorie_tracker.db')
    c = conn.cursor()
    c.execute("""
      SELECT id, user_id, meal_name, calories, proteins, fats, carbs
      FROM meals
      WHERE date(created_at)=date('now')
    """)
    rows = c.fetchall(); conn.close()
    meals = [
      {'id':r[0],'user_id':r[1],'meal_name':r[2],
       'calories':r[3],'proteins':r[4],
       'fats':r[5],'carbs':r[6]}
      for r in rows
    ]
    return jsonify({'meals': meals})

# expose Flask “app” for Vercel Python runtime

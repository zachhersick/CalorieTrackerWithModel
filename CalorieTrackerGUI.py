import tkinter as tk
from tkinter import messagebox
import sqlite3

def getBMR(gender, age, weight, height):
    if gender == "male":
        BMR = 66.5 + (13.75*float(weight)) + (5.003*float(height)) - (6.75*float(age))
        return BMR
    else:
        BMR = 655.1 + (9.563*float(weight)) + (1.850*float(height)) - (4.676*float(age))
        return BMR
    
def getCalories(BMR, activityLevel):
    if activityLevel == 1:
        calories = BMR*1.2
        return calories
    elif activityLevel == 2:
        calories = BMR*1.375
        return calories
    elif activityLevel == 3:
        calories = BMR*1.55
        return calories
    elif activityLevel == 4:
        calories = BMR*1.725
        return calories
    elif activityLevel == 5:
        calories = BMR*1.9
        return calories
    elif activityLevel == 6:
        calories = BMR*2.3
        return calories

def save_user_data(gender, age, weight, height, activity_level, total_calories, total_proteins, total_fats, total_carbs):
    conn = sqlite3.connect('calorie_tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_data (gender, age, weight, height, activity_level, total_calories, total_proteins, total_fats, total_carbs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (gender, age, weight, height, activity_level, total_calories, total_proteins, total_fats, total_carbs))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def save_meal_data(user_id, meal_name, calories, proteins, fats, carbs):
    conn = sqlite3.connect('calorie_tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO meals (user_id, meal_name, calories, proteins, fats, carbs) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, meal_name, calories, proteins, fats, carbs))
    conn.commit()
    conn.close()

def get_last_user_data():
    conn = sqlite3.connect('calorie_tracker.db')
    c = conn.cursor()
    c.execute("SELECT gender, age, weight, height, activity_level, total_calories, total_proteins, total_fats, total_carbs FROM user_data ORDER BY id DESC LIMIT 1")
    data = c.fetchone()
    conn.close()
    return data

class CalorieTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker")

        self.create_widgets()

    def create_widgets(self):
        self.gender_label = tk.Label(self.root, text="Gender:")
        self.gender_label.grid(row=0, column=0)
        self.gender_var = tk.StringVar(value="male")
        self.gender_male = tk.Radiobutton(self.root, text="Male", variable=self.gender_var, value="male")
        self.gender_female = tk.Radiobutton(self.root, text="Female", variable=self.gender_var, value="female")
        self.gender_male.grid(row=0, column=1)
        self.gender_female.grid(row=0, column=2)

        self.age_label = tk.Label(self.root, text="Age:")
        self.age_label.grid(row=1, column=0)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1)

        self.weight_label = tk.Label(self.root, text="Weight (kg):")
        self.weight_label.grid(row=2, column=0)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=2, column=1)

        self.height_label = tk.Label(self.root, text="Height (cm):")
        self.height_label.grid(row=3, column=0)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=3, column=1)

        self.activity_label = tk.Label(self.root, text="Activity Level:")
        self.activity_label.grid(row=4, column=0)
        self.activity_var = tk.IntVar(value=1)
        self.activity_options = [
            "Little/no exercise (sedentary lifestyle)",
            "Light exercise 1-2 times per week",
            "Moderate exercise 2-3 times per week",
            "Hard exercise 4-5 times per week",
            "Physical job or hard exercise 6-7 times per week",
            "Professional athlete"
        ]
        self.activity_menu = tk.OptionMenu(self.root, self.activity_var, *range(1, 7))
        self.activity_menu.grid(row=4, column=1)

        self.protein_label = tk.Label(self.root, text="Percentage of Protein:")
        self.protein_label.grid(row=5, column=0)
        self.protein_entry = tk.Entry(self.root)
        self.protein_entry.grid(row=5, column=1)

        self.carbs_label = tk.Label(self.root, text="Percentage of Carbs:")
        self.carbs_label.grid(row=6, column=0)
        self.carbs_entry = tk.Entry(self.root)
        self.carbs_entry.grid(row=6, column=1)

        self.fat_label = tk.Label(self.root, text="Percentage of Fat:")
        self.fat_label.grid(row=7, column=0)
        self.fat_entry = tk.Entry(self.root)
        self.fat_entry.grid(row=7, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=8, column=0, columnspan=2)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=9, column=0, columnspan=2)

        self.log_meal_button = tk.Button(self.root, text="Log Meal", command=self.log_meal)
        self.log_meal_button.grid(row=10, column=0, columnspan=2)

        self.meal_name_label = tk.Label(self.root, text="Meal Name:")
        self.meal_name_label.grid(row=11, column=0)
        self.meal_name_entry = tk.Entry(self.root)
        self.meal_name_entry.grid(row=11, column=1)

        self.meal_calories_label = tk.Label(self.root, text="Calories:")
        self.meal_calories_label.grid(row=12, column=0)
        self.meal_calories_entry = tk.Entry(self.root)
        self.meal_calories_entry.grid(row=12, column=1)

        self.meal_proteins_label = tk.Label(self.root, text="Proteins (grams):")
        self.meal_proteins_label.grid(row=13, column=0)
        self.meal_proteins_entry = tk.Entry(self.root)
        self.meal_proteins_entry.grid(row=13, column=1)

        self.meal_fats_label = tk.Label(self.root, text="Fats (grams):")
        self.meal_fats_label.grid(row=14, column=0)
        self.meal_fats_entry = tk.Entry(self.root)
        self.meal_fats_entry.grid(row=14, column=1)

        self.meal_carbs_label = tk.Label(self.root, text="Carbs (grams):")
        self.meal_carbs_label.grid(row=15, column=0)
        self.meal_carbs_entry = tk.Entry(self.root)
        self.meal_carbs_entry.grid(row=15, column=1)

    def calculate(self):
        gender = self.gender_var.get()
        age = int(self.age_entry.get())
        weight = float(self.weight_entry.get())
        height = float(self.height_entry.get())
        activity_level = self.activity_var.get()

        BMR = getBMR(gender, age, weight, height)
        total_calories = getCalories(BMR, activity_level)

        percent_protein = int(self.protein_entry.get())
        percent_carbs = int(self.carbs_entry.get())
        percent_fat = int(self.fat_entry.get())

        total_proteins = ((percent_protein / 100) * total_calories) / 4
        total_carbs = ((percent_carbs / 100) * total_calories) / 4
        total_fats = ((percent_fat / 100) * total_calories) / 9

        # Round the values
        rounded_proteins = round(total_proteins)
        rounded_carbs = round(total_carbs)
        rounded_fats = round(total_fats)

        # Adjust the rounding to ensure the total calories still add up
        rounded_total_calories = rounded_proteins * 4 + rounded_carbs * 4 + rounded_fats * 9
        calorie_difference = total_calories - rounded_total_calories

        if calorie_difference != 0:
            if abs(calorie_difference) < 4:
                rounded_proteins += calorie_difference // 4
            elif abs(calorie_difference) < 9:
                rounded_fats += calorie_difference // 9
            else:
                rounded_carbs += calorie_difference // 4

        self.result_label.config(text=f"Total Calories: {total_calories}\nProteins: {rounded_proteins}g\nCarbs: {rounded_carbs}g\nFats: {rounded_fats}g")

        self.user_id = save_user_data(gender, age, weight, height, activity_level, total_calories, rounded_proteins, rounded_fats, rounded_carbs)

    def log_meal(self):
        meal_name = self.meal_name_entry.get()
        meal_calories = float(self.meal_calories_entry.get())
        meal_proteins = float(self.meal_proteins_entry.get())
        meal_fats = float(self.meal_fats_entry.get())
        meal_carbs = float(self.meal_carbs_entry.get())

        save_meal_data(self.user_id, meal_name, meal_calories, meal_proteins, meal_fats, meal_carbs)
        messagebox.showinfo("Meal Logged", "Meal has been logged successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieTrackerApp(root)
    root.mainloop()
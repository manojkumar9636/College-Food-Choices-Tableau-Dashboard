"""
Data Collection & Extraction Script
------------------------------------
Generates a realistic synthetic survey dataset simulating college students'
dietary habits, lifestyle, and academic performance.
This acts as our "database extraction" -> raw_college_food_survey.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 650  # number of student survey responses

majors = ["Engineering", "Commerce", "Arts", "Science", "Medicine"]
years = [1, 2, 3, 4]
genders = ["Male", "Female", "Other"]
breakfast_freq = ["Daily", "Often", "Rarely", "Never"]
cuisine_pref = ["Indian", "Chinese", "Italian", "Continental", "Fast Food", "Mixed"]
eating_location = ["Cafeteria", "Hostel Mess", "Outside", "Home"]
comfort_trigger = ["Stress", "Boredom", "Sadness", "Happiness", "No Trigger"]

rows = []
for i in range(1, N + 1):
    age = np.random.randint(17, 25)
    gender = np.random.choice(genders, p=[0.48, 0.48, 0.04])
    year = np.random.choice(years)
    major = np.random.choice(majors)

    breakfast = np.random.choice(breakfast_freq, p=[0.28, 0.27, 0.30, 0.15])
    meals_per_day = np.random.choice([1, 2, 3, 4], p=[0.05, 0.30, 0.45, 0.20])
    fast_food_per_week = np.random.poisson(3)
    fast_food_per_week = min(fast_food_per_week, 14)
    home_cooked_per_week = max(0, 14 - fast_food_per_week - np.random.randint(0, 5))
    veg_fruit_servings = round(np.random.gamma(2, 1.1), 1)
    veg_fruit_servings = min(veg_fruit_servings, 8)
    calorie_awareness = np.random.choice(["Yes", "No"], p=[0.38, 0.62])
    cuisine = np.random.choice(cuisine_pref)
    location = np.random.choice(eating_location, p=[0.35, 0.25, 0.25, 0.15])
    stress_level = np.random.randint(1, 11)
    trigger_probs = [0.35, 0.25, 0.10, 0.10, 0.20] if stress_level >= 6 else [0.15, 0.20, 0.05, 0.15, 0.45]
    trigger = np.random.choice(comfort_trigger, p=trigger_probs)
    water_intake = round(np.random.normal(2.2, 0.6), 1)
    water_intake = max(0.5, water_intake)
    sleep_hours = round(np.random.normal(6.3, 1.1), 1)
    sleep_hours = max(3, min(10, sleep_hours))
    exercise_per_week = np.random.poisson(2)

    # Concentration influenced by breakfast habit, sleep, stress
    base_conc = 5.0
    if breakfast == "Daily":
        base_conc += 2
    elif breakfast == "Often":
        base_conc += 1
    elif breakfast == "Never":
        base_conc -= 1.5
    base_conc += (sleep_hours - 6.3) * 0.4
    base_conc -= (stress_level - 5) * 0.15
    concentration = int(np.clip(round(base_conc + np.random.normal(0, 1)), 1, 10))

    # Academic performance (CGPA out of 10) influenced by concentration & breakfast
    base_gpa = 6.0 + (concentration - 5) * 0.35 + np.random.normal(0, 0.6)
    if breakfast == "Daily":
        base_gpa += 0.3
    cgpa = round(np.clip(base_gpa, 4.0, 10.0), 2)

    monthly_food_budget = int(np.random.normal(4500, 1200))
    monthly_food_budget = max(1500, monthly_food_budget)

    energy_level = int(np.clip(round(6 + (sleep_hours - 6.3) * 0.5 - (stress_level - 5) * 0.2 + np.random.normal(0, 1)), 1, 10))

    rows.append([
        i, age, gender, year, major, breakfast, meals_per_day, fast_food_per_week,
        home_cooked_per_week, veg_fruit_servings, calorie_awareness, cuisine,
        location, stress_level, trigger, water_intake, sleep_hours, exercise_per_week,
        concentration, cgpa, monthly_food_budget, energy_level
    ])

columns = [
    "StudentID", "Age", "Gender", "AcademicYear", "Major", "BreakfastFrequency",
    "MealsPerDay", "FastFoodPerWeek", "HomeCookedMealsPerWeek", "VegFruitServingsPerDay",
    "CalorieAwareness", "CuisinePreference", "EatingLocation", "StressLevel",
    "ComfortFoodTrigger", "WaterIntakeLiters", "SleepHours", "ExercisePerWeek",
    "ConcentrationLevel", "CGPA", "MonthlyFoodBudgetINR", "EnergyLevel"
]

df = pd.DataFrame(rows, columns=columns)

# Introduce a few realistic missing values (as real survey data would have)
for col in ["VegFruitServingsPerDay", "MonthlyFoodBudgetINR", "SleepHours"]:
    idx = np.random.choice(df.index, size=int(0.02 * N), replace=False)
    df.loc[idx, col] = np.nan

df.to_csv("data/raw_college_food_survey.csv", index=False)
print(f"Generated {len(df)} rows -> data/raw_college_food_survey.csv")

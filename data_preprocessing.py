"""
Data Preparation Script
------------------------
Cleans raw_college_food_survey.csv and produces a Tableau-ready dataset:
data/college_food_survey_clean.csv

Steps performed:
1. Handle missing values (median/mode imputation)
2. Fix data types
3. Create derived/calculated columns useful for visualization
4. Remove duplicates / invalid rows
5. Export clean CSV for Tableau
"""

import pandas as pd
import numpy as np

df = pd.read_csv("data/raw_college_food_survey.csv")

print("Raw shape:", df.shape)
print("Missing values before cleaning:\n", df.isnull().sum())

# 1. Handle missing values
df["VegFruitServingsPerDay"] = df["VegFruitServingsPerDay"].fillna(df["VegFruitServingsPerDay"].median())
df["MonthlyFoodBudgetINR"] = df["MonthlyFoodBudgetINR"].fillna(df["MonthlyFoodBudgetINR"].median())
df["SleepHours"] = df["SleepHours"].fillna(df["SleepHours"].median())

# 2. Remove duplicates
df = df.drop_duplicates(subset="StudentID")

# 3. Derived / calculated columns (also mirror Tableau calculated fields)
df["DietQualityScore"] = (
    (df["VegFruitServingsPerDay"] * 1.5)
    - (df["FastFoodPerWeek"] * 0.5)
    + (df["HomeCookedMealsPerWeek"] * 0.3)
).round(2)

df["IsHealthyEater"] = np.where(df["DietQualityScore"] >= df["DietQualityScore"].median(), "Healthy", "Needs Improvement")

df["PerformanceBand"] = pd.cut(
    df["CGPA"], bins=[0, 6, 7.5, 8.5, 10],
    labels=["Below Average", "Average", "Good", "Excellent"]
)

df["ComfortFoodTrigger"] = df["ComfortFoodTrigger"].fillna("No Trigger")
df["StressEater"] = np.where(df["ComfortFoodTrigger"].isin(["Stress", "Boredom"]), "Yes", "No")

df["SkipsBreakfast"] = np.where(df["BreakfastFrequency"].isin(["Rarely", "Never"]), "Yes", "No")

# 4. Basic sanity filtering (drop impossible values, if any)
df = df[(df["Age"] >= 16) & (df["Age"] <= 30)]
df = df[(df["CGPA"] >= 0) & (df["CGPA"] <= 10)]

# 5. Export clean data
df.to_csv("data/college_food_survey_clean.csv", index=False)

print("\nClean shape:", df.shape)
print("Saved -> data/college_food_survey_clean.csv")
print("\nColumns available for Tableau:\n", list(df.columns))

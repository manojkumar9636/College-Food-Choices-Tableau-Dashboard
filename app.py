"""
Flask Web Integration
----------------------
Serves the project landing page with the embedded Tableau Dashboard and Story.
"""

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

TABLEAU_DASHBOARD_URL = "https://public.tableau.com/app/profile/manoj.kumar5931/viz/CollegeFoodSurveyDashboard/Dashboard1"
TABLEAU_STORY_URL = "https://public.tableau.com/app/profile/manoj.kumar5931/viz/DietaryStrategiesStory/ImprovingPersonalHealthAcademicFocus"


@app.route("/")
def home():
    df = pd.read_csv("data/college_food_survey_clean.csv")
    stats = {
        "total_students": len(df),
        "avg_cgpa": round(df["CGPA"].mean(), 2),
        "pct_skip_breakfast": round((df["SkipsBreakfast"] == "Yes").mean() * 100, 1),
        "pct_stress_eaters": round((df["StressEater"] == "Yes").mean() * 100, 1),
        "avg_fastfood_week": round(df["FastFoodPerWeek"].mean(), 1),
    }
    return render_template("index.html", stats=stats, dashboard_url=TABLEAU_DASHBOARD_URL)


@app.route("/story")
def story():
    return render_template("story.html", story_url=TABLEAU_STORY_URL)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

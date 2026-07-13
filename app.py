"""
Flask Web Integration
----------------------
Serves the project landing page with the embedded Tableau Dashboard and Story.

IMPORTANT: After you publish your workbook to Tableau Public, copy the
"Embed Code" (Share button -> Embed Code) and paste the view URL into
TABLEAU_DASHBOARD_URL and TABLEAU_STORY_URL below.
"""

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# TODO: Replace these with your actual published Tableau Public view URLs
# Example format: "https://public.tableau.com/views/YourWorkbookName/DashboardName"
TABLEAU_DASHBOARD_URL = "https://public.tableau.com/views/YOUR_WORKBOOK/YourDashboard"
TABLEAU_STORY_URL = "https://public.tableau.com/views/YOUR_WORKBOOK/YourStory"


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

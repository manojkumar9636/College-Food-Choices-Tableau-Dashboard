"""
Generates the 10 visualization images (matching TABLEAU_GUIDE.md) from the
cleaned dataset. These serve as ready-made diagrams for the GitHub README /
Screenshots folder, and as a visual reference for rebuilding the same charts
natively in Tableau.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 130

df = pd.read_csv("data/college_food_survey_clean.csv")
os.makedirs("Screenshots", exist_ok=True)

PALETTE = "viridis"

def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"Screenshots/{name}.png", bbox_inches="tight")
    plt.close(fig)

# 1. Bar Chart — Avg CGPA by BreakfastFrequency
order = ["Daily", "Often", "Rarely", "Never"]
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(data=df, x="BreakfastFrequency", y="CGPA", order=order, hue="BreakfastFrequency",
            palette=PALETTE, ax=ax, legend=False, errorbar=None)
ax.set_title("Average CGPA by Breakfast Frequency")
ax.set_ylabel("Average CGPA")
save(fig, "01_avg_cgpa_by_breakfast")

# 2. Pie/Donut — % students by ComfortFoodTrigger
fig, ax = plt.subplots(figsize=(7, 7))
counts = df["ComfortFoodTrigger"].value_counts()
colors = sns.color_palette(PALETTE, len(counts))
ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90, colors=colors,
       wedgeprops={"width": 0.4})
ax.set_title("Students by Comfort Food Trigger")
save(fig, "02_comfort_food_trigger_donut")

# 3. Heat Map — StressLevel vs FastFoodPerWeek
fig, ax = plt.subplots(figsize=(8, 6))
pivot = pd.crosstab(df["StressLevel"], pd.cut(df["FastFoodPerWeek"], bins=[-1,2,4,6,8,20],
                    labels=["0-2","3-4","5-6","7-8","9+"]))
sns.heatmap(pivot, cmap=PALETTE, annot=True, fmt="d", ax=ax)
ax.set_title("Stress Level vs Fast Food Consumption/Week")
ax.set_xlabel("Fast Food Meals/Week")
ax.set_ylabel("Stress Level (1-10)")
save(fig, "03_stress_vs_fastfood_heatmap")

# 4. Box Plot — CGPA distribution by PerformanceBand
fig, ax = plt.subplots(figsize=(7, 5))
band_order = ["Below Average", "Average", "Good", "Excellent"]
sns.boxplot(data=df, x="PerformanceBand", y="CGPA", order=band_order, hue="PerformanceBand",
            palette=PALETTE, ax=ax, legend=False)
ax.set_title("CGPA Distribution by Performance Band")
save(fig, "04_cgpa_boxplot_by_band")

# 5. Scatter — VegFruitServingsPerDay vs ConcentrationLevel colored by IsHealthyEater
fig, ax = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=df, x="VegFruitServingsPerDay", y="ConcentrationLevel",
                 hue="IsHealthyEater", palette="Set2", ax=ax, alpha=0.7)
ax.set_title("Veg/Fruit Intake vs Concentration Level")
save(fig, "05_vegfruit_vs_concentration_scatter")

# 6. Stacked Bar — EatingLocation by AcademicYear
fig, ax = plt.subplots(figsize=(8, 5))
ct = pd.crosstab(df["AcademicYear"], df["EatingLocation"])
ct.plot(kind="bar", stacked=True, colormap=PALETTE, ax=ax)
ax.set_title("Eating Location by Academic Year")
ax.set_xlabel("Academic Year")
ax.set_ylabel("No. of Students")
ax.legend(title="Eating Location", bbox_to_anchor=(1.02, 1), loc="upper left")
save(fig, "06_eating_location_by_year_stacked")

# 7. Line/Area — Avg SleepHours by AcademicYear
fig, ax = plt.subplots(figsize=(7, 5))
sleep_by_year = df.groupby("AcademicYear")["SleepHours"].mean().reset_index()
ax.plot(sleep_by_year["AcademicYear"], sleep_by_year["SleepHours"], marker="o",
        color="#2f6fb5", linewidth=2)
ax.fill_between(sleep_by_year["AcademicYear"], sleep_by_year["SleepHours"], alpha=0.2, color="#2f6fb5")
ax.set_title("Average Sleep Hours by Academic Year")
ax.set_xlabel("Academic Year")
ax.set_ylabel("Avg Sleep Hours")
save(fig, "07_avg_sleep_by_year")

# 8. Tree Map — CuisinePreference by count
try:
    import squarify
    fig, ax = plt.subplots(figsize=(8, 6))
    cuisine_counts = df["CuisinePreference"].value_counts()
    colors = sns.color_palette(PALETTE, len(cuisine_counts))
    squarify.plot(sizes=cuisine_counts.values, label=[f"{i}\n({v})" for i, v in cuisine_counts.items()],
                  color=colors, ax=ax, text_kwargs={"fontsize": 10})
    ax.set_title("Cuisine Preference Distribution (Tree Map)")
    ax.axis("off")
    save(fig, "08_cuisine_preference_treemap")
except ImportError:
    fig, ax = plt.subplots(figsize=(8, 5))
    df["CuisinePreference"].value_counts().plot(kind="bar", color=sns.color_palette(PALETTE, 6), ax=ax)
    ax.set_title("Cuisine Preference Distribution")
    save(fig, "08_cuisine_preference_treemap")

# 9. Bar — Avg MonthlyFoodBudgetINR by Major
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(data=df, x="Major", y="MonthlyFoodBudgetINR", hue="Major", palette=PALETTE,
            ax=ax, legend=False, errorbar=None)
ax.set_title("Average Monthly Food Budget by Major")
ax.set_ylabel("Avg Budget (INR)")
plt.xticks(rotation=20)
save(fig, "09_avg_budget_by_major")

# 10. Bullet/Gauge-style — % StressEater vs target
fig, ax = plt.subplots(figsize=(7, 3))
pct_stress_eater = (df["StressEater"] == "Yes").mean() * 100
target = 30  # target threshold %
ax.barh(["Stress Eaters %"], [100], color="#e0e0e0")
ax.barh(["Stress Eaters %"], [pct_stress_eater], color="#d9534f")
ax.axvline(target, color="black", linestyle="--", linewidth=2, label=f"Target: {target}%")
ax.set_xlim(0, 100)
ax.set_title(f"Stress/Boredom Eaters: {pct_stress_eater:.1f}% (Target: {target}%)")
ax.legend(loc="lower right")
save(fig, "10_stress_eater_bullet")

print("All 10 charts saved in Screenshots/")
for f in sorted(os.listdir("Screenshots")):
    print(" -", f)

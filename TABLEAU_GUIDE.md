# Tableau Build Guide (Step-by-Step)

Use `data/college_food_survey_clean.csv` as your data source. This guide is
mapped directly to the project's Instructions checklist so every requirement
is covered.

## 1. Connect Data
- Open Tableau → **Connect → Text File** → select `college_food_survey_clean.csv`.
- Confirm data types: `StudentID` (String), `Age/CGPA/StressLevel/...` (Number), rest (String/Dimension).

## 2. Calculated Fields (create at least these 4-5)
1. `Diet Quality Score` — already in CSV, but you can recreate:
   `(([VegFruitServingsPerDay]*1.5) - ([FastFoodPerWeek]*0.5) + ([HomeCookedMealsPerWeek]*0.3))`
2. `High Achiever Flag`:
   `IF [CGPA] >= 8.5 THEN "High Achiever" ELSE "Other" END`
3. `Breakfast Impact Group`:
   `IF [BreakfastFrequency] = "Daily" THEN "Regular" ELSEIF [BreakfastFrequency] = "Never" THEN "Skips" ELSE "Occasional" END`
4. `Avg CGPA by Diet` (use as a Table Calculation / LOD):
   `{FIXED [IsHealthyEater] : AVG([CGPA])}`
5. `Fast Food Spend Estimate`:
   `[FastFoodPerWeek] * 150` (assume ₹150/meal — adjust as needed)

## 3. Unique Visualizations (build at least 8-10; one per sheet)
1. **Bar Chart** — Avg CGPA by BreakfastFrequency
2. **Pie/Donut Chart** — % students by ComfortFoodTrigger
3. **Heat Map** — StressLevel vs FastFoodPerWeek (color = count of students)
4. **Box Plot** — CGPA distribution by PerformanceBand
5. **Scatter Plot** — VegFruitServingsPerDay vs ConcentrationLevel (color by IsHealthyEater)
6. **Stacked Bar** — EatingLocation by AcademicYear
7. **Line/Area Chart** — Avg SleepHours by AcademicYear
8. **Tree Map** — CuisinePreference by count of students
9. **Bar Chart** — Avg MonthlyFoodBudgetINR by Major
10. **Bullet/Gauge** — % StressEater vs target threshold

## 4. Dashboard (Responsive Design)
- Create a new **Dashboard**, set size to **Automatic** (for responsiveness).
- Drag in 5-6 of the sheets above (mix of bar/pie/heatmap/scatter).
- Add **Filters**: `AcademicYear`, `Major`, `Gender`, `EatingLocation` — set as
  dashboard-level filters ("Apply to Worksheets → All Using This Data Source").
- Add a **Highlight Action** so clicking one chart filters the others.
- Add a text title box: "College Food Choices — Dietary Insights Dashboard".

## 5. Story (map to the 3 scenarios in the Overview)
Create a **Story** with these scenes (this satisfies "No of Scenes of Story"):
1. **Scene 1 – Personal Health & Academic Focus** (Rahul's scenario) → use the
   Breakfast vs CGPA bar chart.
2. **Scene 2 – Managing Stress-Related Eating** (Priya's scenario) → use the
   ComfortFoodTrigger pie chart + StressLevel heatmap.
3. **Scene 3 – Improving Cafeteria Food Choices** (Cafeteria manager scenario)
   → use the CuisinePreference tree map + EatingLocation stacked bar.
4. **Scene 4 – Recommendations** → summary dashboard with key takeaways as
   captions.

## 6. Performance Testing (document these numbers for submission)
- **Amount of Data Loaded**: 650 rows × 27 columns
- **Utilization of Data Filters**: 4 dashboard filters (AcademicYear, Major, Gender, EatingLocation)
- **No. of Calculation Fields**: 5+ (listed above)
- **No. of Visualizations/Graphs**: 10 sheets + 1 dashboard + 1 story (4 scenes)

## 7. Publish for Web Embedding
- **File → Save to Tableau Public As...** → sign in / create free account → publish.
- Once published, open the workbook on Tableau Public, click **Share**, copy
  the view link. It looks like:
  `https://public.tableau.com/views/YourWorkbookName/DashboardName`
- Paste that URL into `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL` in `app.py`.

# Project Documentation — Step-by-Step Development Procedure

**Author:** Manoj Kumar

## 1. Data Collection & Extraction from Database
- Since a live institutional database was not available, a realistic
  synthetic dataset simulating a student dietary-habits survey was generated
  programmatically (`generate_dataset.py`) with **650 student responses**
  across **22 raw attributes** (demographics, meal habits, stress, sleep,
  academic performance, etc.), with realistic statistical correlations
  (e.g., students who skip breakfast tend to show lower concentration).
- The dataset was connected to Tableau as a flat-file (CSV) data source,
  simulating extraction from a survey/database export.

## 2. Data Preparation
- `data_preprocessing.py` handles:
  - Missing value imputation (median for numeric fields)
  - Duplicate removal
  - 5 new derived columns: `DietQualityScore`, `IsHealthyEater`,
    `PerformanceBand`, `StressEater`, `SkipsBreakfast`
  - Sanity filtering of invalid values
- Output: `data/college_food_survey_clean.csv` (650 rows × 27 columns)

## 3. Data Visualizations
- 10 unique chart types created in Tableau (bar, pie, heatmap, box plot,
  scatter, stacked bar, line, tree map, bullet) — see `TABLEAU_GUIDE.md`
  for exact build steps and field mappings.

## 4. Dashboard
- One responsive dashboard combining 5-6 key visualizations with
  cross-filtering (dashboard actions) and 4 interactive filters
  (AcademicYear, Major, Gender, EatingLocation).

## 5. Story
- A 4-scene Tableau Story mapped directly to the project's 3 real-world
  scenarios (student health, stress eating, cafeteria decisions) plus a
  final recommendations scene.

## 6. Performance Testing
| Metric | Value |
|---|---|
| Amount of Data Loaded | 650 rows × 27 columns |
| Data Filters Used | 4 (AcademicYear, Major, Gender, EatingLocation) |
| Calculated Fields | 5 |
| Visualizations/Graphs | 10 sheets + 1 dashboard + 1 story (4 scenes) |

## 7. Web Integration
- A Flask application (`app.py`) serves a landing page with key summary
  statistics (computed live from the cleaned CSV with pandas) and embeds the
  published Tableau Dashboard and Story using the Tableau Embedding API v3
  (`tableau-viz` web component).
- Routes:
  - `/` — Dashboard view + KPI cards
  - `/story` — Story view

## 8. Project Demonstration & Documentation
- **Explanation video script** (record using screen recorder e.g. OBS/phone):
  1. Introduce the problem: student dietary habits & academic performance.
  2. Walk through `generate_dataset.py` and `data_preprocessing.py` briefly.
  3. Open Tableau, show the 10 visualizations and explain 2-3 key insights.
  4. Show the Dashboard with filters — demonstrate interactivity.
  5. Show the Story — walk through the 3 scenarios.
  6. Run `python app.py`, show the live Flask website with embedded Tableau.
  7. Conclude with recommendations (healthier cafeteria menu, breakfast
     awareness campaigns, stress-management workshops).
- **This document** serves as the step-by-step written procedure.

## Key Insights (for your video/report narrative)
- Students who eat breakfast daily show noticeably higher average
  concentration and CGPA than those who skip it.
- Stress and boredom are the top two triggers for comfort-food consumption.
- Fruit/vegetable intake is low across the board while fast-food consumption
  is high — supporting the case for better cafeteria options.

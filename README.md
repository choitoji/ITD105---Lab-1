Project Summary
Name: Paman, Xander Cage M.
Subject and Section: ITD105 – IT4D.1
Course: ITD105 – Big Data Analytics
Lab Exercise: #1 – Exploratory Data Analysis (EDA) of Student Exam Performance

Overview
The goal of this project is to perform an exploratory data analysis on student exam performance using a dataset of student information and exam scores. A Streamlit application is created to load, visualize, and interact with the data.

Tasks and Activities
Install Required Libraries
Use pip to install the necessary libraries:

bash
Copy
pip install streamlit pandas matplotlib seaborn plotly
Download the Dataset

Dataset file: student-mat.csv
Link: Google Drive
Set Up the Streamlit App

Create a new Python file (e.g., student_performance.py).
Import the libraries and set up the basic structure of your Streamlit app.
Exploratory Data Analysis

Load and Display the Data: Show the first few rows and dataset info (data types, missing values).
Summary Statistics: Describe numerical columns for measures such as mean, median, and standard deviation.
Heatmap: Visualize correlations between features to identify potential relationships.
Boxplot: Observe the spread and outliers for numeric features like G1, G2, G3 scores.
Interactive Scatter Plot (Plotly): Explore relationships (e.g., study time vs. exam score).
Key Findings and Insights
Feature Correlation with Final Exam Scores

Highest correlation with G1, G2, and G3: Study time has a positive impact on exam performance.
Study Time vs. Exam Performance

Positive correlation indicates that the more a student studies, the better their exam scores.
Insights from the Boxplot

G3 shows a significant range where many students achieve higher scores.
G2 has a shorter range, suggesting most scores are closer to the average.
G1 varies more widely compared to G2.
Impact of Gender on Final Exam Scores

Study Time observations:
In G1: Female students tend to have a higher study time.
In G2 & G3: Male students tend to have a higher study time.
Mean Exam Scores: Male students performed slightly better than female students on average, despite some differences in study time distribution.
Grade Booster (Suggested Enhancements)
Interactive Filters: Add widgets (e.g., selectbox, sliders) in Streamlit to filter by gender, parental education, and other features.
Additional Visualizations: Incorporate bar charts and pair plots for deeper feature comparisons.
Dashboard Layout: Use columns, tabs, and other Streamlit layout options to make the interface more user-friendly and interactive.
Submission Requirements
Source Code: (e.g., student_performance.py)
Google Drive Link (Code): Link
Video Demonstration (max 2 minutes): Link

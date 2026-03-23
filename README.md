Project Name : CrimeSight

CrimeSight is an interactive crime analysis and visualization web application that helps users explore crime patterns, trends, and cyber attack statistics through dynamic charts and data filtering. The system allows users to analyze crime data across states, districts, years, and categories to better understand crime distribution and cyber security threats.

The main objective of CrimeSight is to transform raw crime datasets into meaningful visual insights that are easy to interpret. By using interactive charts and filtering options, users can quickly identify crime trends, compare regions, and study different types of cyber attacks.

Features : 
A. IPC Crime Analysis :
1. State Crime Overview : Displays the distribution of different crimes in a selected state and year.
2. Crime Trend Analysis : Shows how a specific crime changes over time in a selected district.
3. Top States Ranking : Displays the top states with the highest crime counts for a selected crime.
4. District Ranking : Shows districts with the highest crime occurrences within a selected state.
B. Cyber Crime Analysis :
1. Cyber Attacks Overview : Displays the distribution of different types of cyber attacks.
2. Industry and Target Analysis : Shows which industries or targets are most affected by cyber attacks.
3. Data Loss and Severity Analysis : Helps understand the impact level and severity of cyber incidents.
4. Mitigation Methods and Outcome Analysis : Shows how cyber attacks were mitigated and their outcomes.

Visualization Support :

CrimeSight provides multiple chart types for better data understanding:

Bar Chart
Line Chart
Horizontal Bar Chart
Pie Chart

Users can also customize chart colors and export visualizations.

Technologies Used : 

Frontend :
Svelte
Chart.js

Backend :
FastAPI (Python)

Data Processing :
Pandas 

Dataset : 
IPC : https://www.kaggle.com/datasets/meruvulikith/crimes-in-india-dataset-2001-2013
Cyber : https://www.kaggle.com/datasets/shakirul09/cyber-crimes-dataset

Project Structure : 
CrimeSight : 
│
├── backend
│   ├── main.py
│   ├── routes
│   └── datasets
│
├── frontend
│   ├── src
│   ├── components
│   └── pages
│
├── charts
├── static
└── README.md

Key Functionalities :
1. Interactive data filtering
2. Multiple chart visualizations
3. Dynamic data loading
4. Export chart option
5. Clean and user friendly interface
6. Purpose of the Project

CrimeSight is designed to help researchers, students, and analysts explore crime datasets easily. By presenting crime data through visual analytics, the platform makes it easier to identify patterns, compare regions, and understand crime trends over time.
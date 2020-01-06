# TempeSurveyReport
Overview
The city of Tempe, AZ has gathered survey data on employees. I’m going to load it into a postgres database and then analyze it using python, pandas, and sklearn. If I have time I will convert the pandas code to spark. The output of the project will be an automatically generated pdf based on the statistics of user selected questions.

Research Questions
Reasons for attrition, can attrition rates correlate to survey results?
Productivity, can it be measured and correlated to survey results?
Happiness, can it be measured and correlated to survey results?

Survey Improvements
Is there redundancy in the survey?
Do certain survey questions correlate very highly?

Clustering
Can employees be grouped into two or three groups?
How much information is lost in a PCA?

Statistics
What are the quartiles, means, maximums, and minimums for the questions?
What are the quartiles, means, maximums, and minimums for each group?

Database
What is the best database schema for this problem?
Maybe something similar to this: https://stackoverflow.com/questions/1764435/database-design-for-a-survey
Build a diagram of schema for the read me
Build and load the database using SQL alchemy

Data Cleaning
Clean up the questions by using the text data

Report
Generate report with graphs
Barchart of answers for any given question
Chart of stats
Ability to select questions
Ability to list Questions
Dynamic sentence generation based on insights?

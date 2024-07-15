#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load
school_data_to_load = "./Resources/schools_complete.csv"
student_data_to_load = "./Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)
# school_data
# student_data


# In[2]:


school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
# school_data_complete


# In[3]:


# rename school name column
school_data_complete = school_data_complete.rename(columns={"school_name" : "School Name"})
# school_data_complete


# ## District Summary

# In[5]:


# Calculate the total number of unique schools
school_count = len(school_data_complete["School Name"].unique())
# school_count


# In[6]:


# Calculate the total number of students
student_count = len(school_data_complete["Student ID"].unique() )
# student_count


# In[10]:


# Calculate the total budget
total_budget = school_data["budget"].sum()
# total_budget


# In[13]:


# Calculate the average (mean) math score
average_math_score = school_data_complete["math_score"].mean()
# average_math_score


# In[14]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete["reading_score"].mean()
# average_reading_score


# In[18]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["Student ID"]
# passing_math_count
passing_math_percentage = passing_math_count / float(student_count) * 100
# passing_math_percentage


# In[20]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["Student ID"]
# passing_reading_count
passing_reading_percentage = passing_reading_count / float(student_count) * 100
# passing_reading_percentage


# In[22]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
# passing_math_reading_count
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
# overall_passing_rate


# In[24]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame({"Total Schools" : [school_count],
                                 "Total Students" : [student_count],
                                 "Total Budget" : [total_budget],
                                 "Average Math Score" : [average_math_score],
                                 "Average Reading Score" : [average_reading_score],
                                 "% Passing Math" : [passing_math_percentage],
                                 "% Passing Reading" : [passing_reading_percentage],
                                 "% Overall Passing" : [overall_passing_rate] 
                                })


# In[26]:


# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.0f}".format)
district_summary["Average Math Score"] = district_summary["Average Math Score"].map("{:.2f}".format)
district_summary["Average Reading Score"] = district_summary["Average Reading Score"].map("{:.2f}".format)
district_summary["% Passing Math"] = district_summary["% Passing Math"].map("{:.2f}%".format)
district_summary["% Passing Reading"] = district_summary["% Passing Reading"].map("{:.2f}%".format)
district_summary["% Overall Passing"] = district_summary["% Overall Passing"].map("{:.2f}%".format)

# drop index column?
# district_summary.drop(index, axis=1)


# In[28]:


# Display the DataFrame
district_summary


# In[30]:


# Print df to terminal when running code .py file in terminal
print("District Summary:")
print(district_summary.to_markdown())


# ## School Summary

# In[33]:


# rename school name column
school_data = school_data.rename(columns={"school_name" : "School Name"})
# school_data.head()


# In[35]:


# Use the code provided to select the type per school from school_data
# school_data = school_data.rename(columns={"school_name":"School Name"})
school_types = school_data.set_index(["School Name"])["type"]
# school_types


# In[37]:


# Calculate the total student count per school from school_data
per_school_students = school_data_complete["School Name"].value_counts()
# per_school_students


# In[39]:


# Calculate the total school budget per school from school_data
per_school_budget = school_data_complete.groupby(["School Name"]).mean(numeric_only=True)["budget"]
# per_school_budget 


# In[41]:


# Calculate the per capita spending per school from school_data
per_school_capita = per_school_budget / per_school_students
# per_school_capita


# In[43]:


# Calculate the average math test scores per school from school_data_complete
per_school_math = school_data_complete.groupby(["School Name"]).mean(numeric_only=True)["math_score"]
# per_school_math


# In[45]:


# Calculate the average reading test scores per school from school_data_complete
per_school_reading = school_data_complete.groupby(["School Name"]).mean(numeric_only=True)["reading_score"]
# per_school_reading


# In[47]:


# Calculate the number of students per school with math scores of 70 or higher from school_data_complete
students_passing_math = school_data_complete[school_data_complete["math_score"] >= 70]
# students_passing_math

school_students_passing_math = students_passing_math.groupby(["School Name"]).size()
# school_students_passing_math

# Use the provided code to calculate the passing rates PASSING MATH
per_school_passing_math = school_students_passing_math / per_school_students * 100
# per_school_passing_math


# In[49]:


# Calculate the number of students per school with reading scores of 70 or higher from school_data_complete
students_passing_reading = school_data_complete[school_data_complete["reading_score"] >= 70]
# students_passing_reading

school_students_passing_reading = students_passing_reading.groupby(["School Name"]).size()
# school_students_passing_reading

# Use the provided code to calculate the passing rates PASSING READING
per_school_passing_reading = school_students_passing_reading / per_school_students * 100
# per_school_passing_reading


# In[51]:


# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)]
# students_passing_math_and_reading

school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["School Name"]).size()
# school_students_passing_math_and_reading

# Use the provided code to calculate the passing rates PASSING MATH & READING
overall_passing_rate = school_students_passing_math_and_reading / per_school_students * 100
# overall_passing_rate


# In[53]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = pd.DataFrame({"School Type" : school_types ,
                                   "Total Students" : per_school_students ,
                                   "Total School Budget" : per_school_budget ,
                                   "Per Student Budget" : per_school_capita , 
                                   "Average Math Score" : per_school_math ,
                                   "Average Reading Score" : per_school_reading , 
                                   "% Passing Math" : per_school_passing_math ,
                                   "% Passing Reading" : per_school_passing_reading ,
                                   "% Passing Overall" : overall_passing_rate
                                    })


# In[55]:


# Formatting
per_school_summary["Total Students"] = per_school_summary["Total Students"].map("{:,.0f}".format)
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.0f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.0f}".format)
per_school_summary["Average Math Score"] = per_school_summary["Average Math Score"].map("{:,.2f}".format)
per_school_summary["Average Reading Score"] = per_school_summary["Average Reading Score"].map("{:,.2f}".format)
per_school_summary["% Passing Math"] = per_school_summary["% Passing Math"].map("{:,.2f}".format)
per_school_summary["% Passing Reading"] = per_school_summary["% Passing Reading"].map("{:,.2f}".format)
per_school_summary["% Passing Overall"] = per_school_summary["% Passing Overall"].map("{:,.2f}".format)

# per_school_summary.index.name = None


# In[57]:


# Display the DataFrame
per_school_summary


# In[59]:


# Print df to terminal when running code .py file in terminal
print("-")
print("School Summary:")
print(per_school_summary.to_markdown())


# ## Highest-Performing Schools (by % Overall Passing)

# In[163]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(["% Passing Overall"], ascending=False)
top_schools.head(5)


# In[165]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Top 5 Performing Schools by % Overall Passing:")
print(top_schools.head(5).to_markdown())


# ## Bottom Performing Schools (By % Overall Passing)

# In[67]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(["% Passing Overall"], ascending=True)
bottom_schools.head(5)


# In[69]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Bottom 5 Performing Schools by % Overall Passing:")
print(bottom_schools.head(5).to_markdown())


# ## Math Scores by Grade

# In[72]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]
# twelfth_graders


# In[74]:


# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grade_math_scores = ninth_graders.groupby(["School Name"]).mean(numeric_only=True)["math_score"]
tenth_grade_math_scores = tenth_graders.groupby(["School Name"]).mean(numeric_only=True)["math_score"]
eleventh_grade_math_scores = eleventh_graders.groupby(["School Name"]).mean(numeric_only=True)["math_score"]
twelfth_grade_math_scores = twelfth_graders.groupby(["School Name"]).mean(numeric_only=True)["math_score"]
# twelfth_grade_math_scores


# In[76]:


# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({"9th Grade" : ninth_grade_math_scores ,
                                   "10th Grade" : tenth_grade_math_scores ,
                                   "11th Grade" : eleventh_grade_math_scores ,
                                   "12th Grade" : twelfth_grade_math_scores 
                                    })


# In[78]:


# Formatting
math_scores_by_grade["9th Grade"] = math_scores_by_grade["9th Grade"].map("{:,.2f}".format)
math_scores_by_grade["10th Grade"] = math_scores_by_grade["10th Grade"].map("{:,.2f}".format)
math_scores_by_grade["11th Grade"] = math_scores_by_grade["11th Grade"].map("{:,.2f}".format)
math_scores_by_grade["12th Grade"] = math_scores_by_grade["12th Grade"].map("{:,.2f}".format)

# Minor data wrangling
# math_scores_by_grade.index.name = None


# In[80]:


# Display the DataFrame
math_scores_by_grade


# In[82]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Math Scores by Grade:")
print(math_scores_by_grade.to_markdown())


# ## Reading Score by Grade 

# In[85]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]


# In[87]:


# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_scores = ninth_graders.groupby(["School Name"]).mean(numeric_only=True)["reading_score"]
tenth_grade_reading_scores = tenth_graders.groupby(["School Name"]).mean(numeric_only=True)["reading_score"]
eleventh_grade_reading_scores = eleventh_graders.groupby(["School Name"]).mean(numeric_only=True)["reading_score"]
twelfth_grade_reading_scores = twelfth_graders.groupby(["School Name"]).mean(numeric_only=True)["reading_score"]
# ninth_grade_reading_scores


# In[89]:


# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({"9th Grade" : ninth_grade_reading_scores ,
                                   "10th Grade" : tenth_grade_reading_scores ,
                                   "11th Grade" : eleventh_grade_reading_scores ,
                                   "12th Grade" : twelfth_grade_reading_scores 
                                    })


# In[91]:


# Formatting
reading_scores_by_grade["9th Grade"] = reading_scores_by_grade["9th Grade"].map("{:,.2f}".format)
reading_scores_by_grade["10th Grade"] = reading_scores_by_grade["10th Grade"].map("{:,.2f}".format)
reading_scores_by_grade["11th Grade"] = reading_scores_by_grade["11th Grade"].map("{:,.2f}".format)
reading_scores_by_grade["12th Grade"] = reading_scores_by_grade["12th Grade"].map("{:,.2f}".format)

# Minor data wrangling
# reading_scores_by_grade = reading_scores_by_grade[["9th Grade", "10th Grade", "11th Grade", "12th Grade"]]
# reading_scores_by_grade.index.name = None


# In[93]:


# Display the DataFrame
reading_scores_by_grade


# In[95]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Reading Scores by Grade:")
print(reading_scores_by_grade.to_markdown())


# ## Scores by School Spending

# In[98]:


# Establish the bins
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[100]:


# Create a copy of the school summary since it has the "Per Student Budget"
school_spending_df = per_school_summary.copy()
# school_spending_df.dtypes


# In[102]:


# convert columns to float for further calculations
school_spending_df = school_spending_df.astype({"Average Math Score": "float",
                         "Average Reading Score": "float",
                         "% Passing Math": "float", 
                         "% Passing Reading": "float",
                         "% Passing Overall": "float" })
# school_spending_df


# In[104]:


# pd.cut(per_school_capita, bins=spending_bins, labels=labels)


# In[106]:


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(per_school_capita, bins=spending_bins, labels=labels)
# school_spending_df.head()


# In[108]:


# school_spending_df.dtypes


# In[110]:


#  Calculate averages for the desired columns.
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"] , observed=False)["Average Math Score"].mean(numeric_only=True)
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"] , observed=False)["Average Reading Score"].mean(numeric_only=True)
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"] , observed=False)["% Passing Math"].mean(numeric_only=True)
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"] , observed=False)["% Passing Reading"].mean(numeric_only=True)
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"] , observed=False)["% Passing Overall"].mean(numeric_only=True)
# spending_passing_reading


# In[112]:


# Assemble into DataFrame
spending_summary = pd.DataFrame({"Average Math Score" : spending_math_scores ,
                                   "Average Reading Score" : spending_reading_scores ,
                                   "% Passing Math" : spending_passing_math ,
                                   "% Passing Reading" : spending_passing_reading,
                                   "% Passing Overall" : overall_passing_spending
                                    })


# In[114]:


# Formatting
spending_summary["Average Math Score"] = spending_summary["Average Math Score"].map("{:,.2f}".format)
spending_summary["Average Reading Score"] = spending_summary["Average Reading Score"].map("{:,.2f}".format)
spending_summary["% Passing Math"] = spending_summary["% Passing Math"].map("{:,.2f}%".format)
spending_summary["% Passing Reading"] = spending_summary["% Passing Reading"].map("{:,.2f}%".format)
spending_summary["% Passing Overall"] = spending_summary["% Passing Overall"].map("{:,.2f}%".format)


# In[116]:


# Display results
spending_summary


# In[118]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Scores by School Spending:")
print(spending_summary.to_markdown())


# ## Scores by School Size

# In[121]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[123]:


school_size_df = per_school_summary.copy()


# In[125]:


# pd.cut(per_school_students, bins=size_bins, labels=labels)


# In[127]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

school_size_df["School Size"] = pd.cut(per_school_students, bins=size_bins, labels=labels)
# school_size_df.head()


# In[129]:


# school_size_df.dtypes


# In[131]:


#reset columns to Float instead of object for further calculations
school_size_df = school_size_df.astype({"Average Math Score": "float",
                         "Average Reading Score": "float",
                         "% Passing Math": "float", 
                         "% Passing Reading": "float",
                         "% Passing Overall": "float" })
# school_size_df.dtypes


# In[133]:


# Calculate averages for the desired columns.
size_math_scores = school_size_df.groupby(["School Size"] , observed=False)["Average Math Score"].mean(numeric_only=True)
size_reading_scores = school_size_df.groupby(["School Size"] , observed=False)["Average Reading Score"].mean(numeric_only=True)
size_passing_math = school_size_df.groupby(["School Size"] , observed=False)["% Passing Math"].mean(numeric_only=True)
size_passing_reading = school_size_df.groupby(["School Size"] , observed=False)["% Passing Reading"].mean(numeric_only=True)
size_overall_passing = school_size_df.groupby(["School Size"] , observed=False)["% Passing Overall"].mean(numeric_only=True)


# In[135]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({"Average Math Score" : size_math_scores ,
                                   "Average Reading Score" : size_reading_scores ,
                                   "% Passing Math" : size_passing_math ,
                                   "% Passing Reading" : size_passing_reading,
                                   "% Passing Overall" : size_overall_passing
                            })


# In[137]:


# Formatting
size_summary["Average Math Score"] = size_summary["Average Math Score"].map("{:,.2f}".format)
size_summary["Average Reading Score"] = size_summary["Average Reading Score"].map("{:,.2f}".format)
size_summary["% Passing Math"] = size_summary["% Passing Math"].map("{:,.2f}%".format)
size_summary["% Passing Reading"] = size_summary["% Passing Reading"].map("{:,.2f}%".format)
size_summary["% Passing Overall"] = size_summary["% Passing Overall"].map("{:,.2f}%".format)


# In[139]:


# Display results
size_summary


# In[141]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Scores by School Size:")
print(size_summary.to_markdown())


# ## Scores by School Type

# In[144]:


# new df for School Type
school_type_df = per_school_summary.copy()
# school_type_df


# In[146]:


# school_type_df.dtypes


# In[148]:


#reset columns to Float instead of object for further calculations
school_type_df = school_type_df.astype({"Average Math Score": "float",
                         "Average Reading Score": "float",
                         "% Passing Math": "float", 
                         "% Passing Reading": "float",
                         "% Passing Overall": "float" })
# school_type_df


# In[150]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = school_type_df.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = school_type_df.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = school_type_df.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = school_type_df.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = school_type_df.groupby(["School Type"])["% Passing Overall"].mean()


# In[152]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({"Average Math Score" : average_math_score_by_type ,
                                   "Average Reading Score" : average_reading_score_by_type ,
                                   "% Passing Math" : average_percent_passing_math_by_type ,
                                   "% Passing Reading" : average_percent_passing_reading_by_type,
                                   "% Passing Overall" : average_percent_overall_passing_by_type
                            })


# In[154]:


# Formatting
type_summary["Average Math Score"] = type_summary["Average Math Score"].map("{:,.2f}".format)
type_summary["Average Reading Score"] = type_summary["Average Reading Score"].map("{:,.2f}".format)
type_summary["% Passing Math"] = type_summary["% Passing Math"].map("{:,.2f}%".format)
type_summary["% Passing Reading"] = type_summary["% Passing Reading"].map("{:,.2f}%".format)
type_summary["% Passing Overall"] = type_summary["% Passing Overall"].map("{:,.2f}%".format)


# In[156]:


# Display results
type_summary


# In[158]:


# Print df to terminal when running code .py file in terminal
print("-")
print("Scores by School Type:")
print(type_summary.to_markdown())


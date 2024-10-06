import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
github_data = pd.read_csv('github_dataset.csv')
repo_data = pd.read_csv('repository_data.csv')

# Data preprocessing
# Fill missing values in 'language' with 'Unknown'
github_data['language'] = github_data['language'].fillna('Unknown')

# Merge the datasets on common key, assuming repositories correspond by name
# We might need to adjust the matching if the names are different
merged_data = pd.merge(github_data, repo_data, left_on='repositories', right_on='name', how='outer')

# Basic Overview
st.title("GitHub Repository Insights Dashboard")
st.write("This dashboard provides insights into GitHub repositories, including stars, forks, pull requests, and language usage.")

# Top Repositories by Stars
st.subheader("Top Repositories by Stars")
top_star_repos = repo_data.nlargest(10, 'stars_count')[['name', 'stars_count']]
st.write(top_star_repos)

# Stars vs Forks visualization
st.subheader("Stars vs Forks")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='stars_count', y='forks_count', data=repo_data)
plt.title('Stars vs Forks Count')
plt.xlabel('Stars')
plt.ylabel('Forks')
st.pyplot(plt)

# Language Distribution with "Others" category for smaller percentages
st.subheader("Repository Language Distribution (with 'Others')")

# Calculate the percentage of each language
language_counts = github_data['language'].value_counts()
total_repos = language_counts.sum()
language_percentages = (language_counts / total_repos) * 100

# Set a threshold of 2.5% for grouping into "Others"
threshold = 2.5
large_languages = language_percentages[language_percentages >= threshold]
small_languages = language_percentages[language_percentages < threshold]

# Combine small percentages into "Others" using concat instead of append
combined_languages = pd.concat([large_languages, pd.Series(small_languages.sum(), index=['Others'])])

# Plot the pie chart
fig, ax = plt.subplots()
ax.pie(combined_languages, labels=combined_languages.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Repository Language Distribution (Languages < 2.5% combined as "Others")')
st.pyplot(fig)


# Filter by Language
st.subheader("Filter Repositories by Language")
selected_language = st.selectbox('Select Language', github_data['language'].unique())
filtered_data = github_data[github_data['language'] == selected_language]
st.write(filtered_data[['repositories', 'stars_count', 'forks_count', 'issues_count']])

# Correlation between Stars and Pull Requests
st.subheader("Correlation between Stars and Pull Requests")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='stars_count', y='pull_requests', data=repo_data)
plt.title('Stars vs Pull Requests')
plt.xlabel('Stars')
plt.ylabel('Pull Requests')
st.pyplot(plt)

# Footer
st.write("Dashboard created by Harish using Streamlit.")

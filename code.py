import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
df = pd.read_csv("C:\\Users\\singa\\Documents\\OneDrive\\Desktop\\python project.csv", encoding='ISO-8859-1')
# 1:Data Cleaning & Preprocessing

print(df.info())
print("\nMissing Values:")
print(df.isnull().sum())

df['size'] = df['size'].str.replace('\x96', '-', regex=True)

df['line_code'] = df['line_code'].fillna(df['line_code'].mode()[0])
df['industry'] = df['industry'].fillna(df['industry'].mode()[0])
df['size'] = df['size'].fillna(df['size'].mode()[0])
df['level'] = df['level'].fillna(df['level'].mean())
df['description'] = df['description'].fillna(df['description'].mode()[0])
df['value'] = df['value'].fillna(df['value'].mean())

df.drop_duplicates(inplace=True)

z = np.abs(stats.zscore(df[['level', 'value']]))
df = df[(z < 3).all(axis=1)]

print("\nCleaned Data Info:")
print(df.info())
print("Remaining null values:", df.isnull().sum().sum())

# 2:Exploratory Data Analysis (EDA)

print("\n--- Descriptive Statistics ---")
print(df.describe())

# Value distribution (Histogram)
plt.figure()
sns.histplot(df['value'], bins=30, kde=True)
plt.title("Distribution of Financial Values (Histogram)")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Count by industry (Bar Chart)
plt.figure(figsize=(10, 8))
sns.countplot(y='industry', data=df, order=df['industry'].value_counts().index)
plt.title("Record Count by Industry (Bar Chart)")
plt.tight_layout()
plt.show()

# 3:Financial Insights Extraction
total = df['value'].sum()
average = df['value'].mean()
maximum = df['value'].max()

print("\n--- Financial Insights ---")
print(f"Total Value: {total}")
print(f"Average Value: {average}")
print(f"Maximum Value: {maximum}")

# 4:Data Visualization
industry_values = df.groupby('industry')['value'].sum().sort_values()

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(industry_values.values, industry_values.index, color='teal')  # x: values, y: industries
plt.title("Total Value by Industry (Scatter Plot)")
plt.xlabel("Value")
plt.ylabel("Industry")
plt.tight_layout()
plt.show()

##pie chart
size_counts = df['size'].value_counts()
colors = plt.cm.Set3(np.linspace(0, 1, len(size_counts)))
plt.figure(figsize=(8, 8))
plt.pie(
    size_counts,
    labels=size_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    textprops={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}
)

plt.title("Business Size Distribution (Pie Chart)", fontsize=14, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

##Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='size', y='value', data=df)
plt.title("Value by Business Size (Box Plot)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Line Graph
df_sorted = df.sort_values(by='level')
plt.figure(figsize=(8, 5))
plt.plot(df_sorted['level'], df_sorted['value'], marker='o', color='blue')
plt.title("Level vs Value (Line Graph)")
plt.xlabel("Level")
plt.ylabel("Value")
plt.grid(True)
plt.tight_layout()
plt.show()

# 5:Business Decision Support

print("\n--- Business Decision Support ---")

print("\nTop Industries by Revenue:")
print(df.groupby('industry')['value'].sum().sort_values(ascending=False).head())

print("\nTop Business Sizes by Revenue:")
print(df.groupby('size')['value'].sum().sort_values(ascending=False))

print("\nTop Line Codes by Revenue:")
print(df.groupby('line_code')['value'].sum().sort_values(ascending=False).head(10))

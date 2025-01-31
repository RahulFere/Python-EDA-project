#Lbraries Used:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

#Loading Dataset
df=pd.read_csv("retail_store_sales.csv")


#Data Overview:
print("df.dataset information")
print(df.info())

print("\Dataset Information:\n")
print(df.describe())

print("Missing Values\n")
print(df.isnull().sum())

#Fill Missing Values:
for col in df.select_dtypes(include=["number"]):
    df[col].fillna(df[col].mean(),inplace=True)

for col in df.select_dtypes(include=['object']):
    df[col].fillna(df[col].mode(),inplace=True)



for item in df:
    df[item]=df[item].fillna("UNKNOWN")

#Convert Date Columns to Datetime format
df["Transaction Date"]=df["Transaction Date"].astype('datetime64[ns]')

#Adding new features:


df['order_year'] = df['Transaction Date'].dt.year
print(df['order_year'])
df['order_month'] = df['Transaction Date'].dt.month
print(df['order_month'])
df['order_weekday'] = df['Transaction Date'].dt.day_name()
print(df['order_weekday'])
df['returning_customer'] = df.duplicated(subset=['Customer ID'], keep=False)
print(df['returning_customer'])

#Sales by Product Catagory

sales_by_category = df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
print("\nSales by Category:\n", sales_by_category)

# Money Collected by a product Category
Money_Collected_by_a_product_Category = df.groupby('Category')['Total Spent'].sum().sort_values(ascending=False)
print("\nMoney Collected by a product Categorys:\n", Money_Collected_by_a_product_Category )

#Sales by Location
sales_by_location = df.groupby('Location')['Quantity'].sum().sort_values(ascending=False)
print("\nSales by location:\n", sales_by_location)



#  Univariate Analysis
numerical_cols = ['Price Per Unit', 'Quantity', 'Total Spent']
for col in numerical_cols:
    plt.figure(figsize=(8, 4))
    sb.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.show()


categorical_cols = ['Category', 'Payment Method', 'Location']
for col in categorical_cols:
    plt.figure(figsize=(8, 4))
    value_counts = df[col].value_counts()
    plt.bar(value_counts.index, value_counts.values, color='skyblue')
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()


# Bivariate Analysis


plt.figure(figsize=(10, 6))
sb.barplot(x=Money_Collected_by_a_product_Category.index, y=Money_Collected_by_a_product_Category.values, palette="viridis")
plt.title('Money Collected by a product Category', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.xticks(rotation=45)
plt.show()



plt.figure(figsize=(8, 4))
sb.barplot(x='Category', y='Quantity', data=df, ci=None)
plt.title("Sales by Category")
plt.xticks(rotation=45)
plt.show()


#  Multivariate Analysis
numerical_cols_filtered = [col for col in numerical_cols if col in df.columns]
sb.pairplot(df[numerical_cols_filtered])
plt.show()


# Time-Based Analysis
df['order_month'] = df['Transaction Date'].dt.to_period('M')
sales_trends = df.groupby('order_month')['Quantity'].sum()

plt.figure(figsize=(12, 6))
sales_trends.plot()
plt.title("Sales Trend Over Time")
plt.xlabel("Order Month")
plt.ylabel("Total Sales")
plt.grid()
plt.show()


# Customer Behavior Analysis
customer_spend = df.groupby('Customer ID')['Quantity'].sum()
print("\nTop 10 Customers by Spending:\n", customer_spend.sort_values(ascending=False).head(10))



#Reporting Insights
print("\nTop Insights:")
print("1. Top performing categories:\n", sales_by_category)
print("3. Year-over-Year Sales Growth:\n", df.groupby('order_year')['Total Spent'].sum().pct_change())



#Monthly Sales Trend
monthly_sales = df.groupby(['order_year', 'order_month'])['Quantity'].sum().reset_index()
print("Monthly Sales Trend:\n", monthly_sales)

#Product Performance Comparison
product_sales = df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
print("Product Sales Performance:\n", product_sales)


# Save Cleaned Data
df.to_csv("cleaned_retail_store_sales.csv", index=False)













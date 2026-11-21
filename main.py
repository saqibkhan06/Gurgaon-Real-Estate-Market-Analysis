import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv') # Load the dataset

# Data Cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df = df.drop_duplicates() # Drop duplicate rows

# Numerical Columns Cleaning
df['price'] = df["price"].astype(str).str.replace(",", "").astype(float) # Convert price to float after removing commas
df['area'] = df["area"].astype(str).str.replace(",", "").astype(int) # Convert area to int after removing commas
df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(",", "").astype(int) # Convert rate_per_sqft to int after removing commas


# Categorical Columns Cleaning
df['status'] = df['status'].str.strip().str.lower() # Standardize status column
df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False}) # Convert RERA approval to boolean
df['flat_type'] = df['flat_type'].str.strip().str.lower() # Standardize flat_type column

df = df.drop_duplicates() # Drop duplicate rows again after cleaning

# print(df)
# print(df.info())

# Question 1: Which is the costliest flat in the dataset?
costliest_flat = df.loc[df['price'].idxmax()] # Get the row with the maximum price
print(f"The costliest flat is a {costliest_flat['bhk_count']} BHK flat located in {costliest_flat['locality']} priced at {costliest_flat['price']/10000000} crores in {costliest_flat['society']} society.")

# Question 2: Which locality has the highest average price?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax() # Get the locality with the highest average price
print(f"The locality with the highest average price is {highest_avg_price_locality}.")

# Question 3: Which locality has the highest rate per square foot?
highest_rate_locality = df.groupby('locality')['rate_per_sqft'].mean().idxmax() # Get the locality with the highest rate per square foot
print(f"The locality with the highest rate per square foot is {highest_rate_locality}.")

# Question 4: Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean() # Get the average price for ready-to-move properties
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean() # Get the average price for under-construction properties

if ready_to_move_avg_price > under_construction_avg_price:
    print("Ready-to-move properties cost more on average than under-construction properties.")
else:
    print("Under-construction properties cost more on average than ready-to-move properties.")

# Question 5: Do RERA-approved properties command a price premium?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean() # Get the average price for RERA-approved properties
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean() # Get the average price for non-RERA-approved properties

if rera_approved_avg_price > rera_not_approved_avg_price:
    print("RERA-approved properties command a price premium.")
else:
    print("RERA-approved properties do not command a price premium.")

# Question 6: How does area impact price?
# sns.scatterplot(data=df, x='area', y='price') # Create a scatter plot of area vs. price
# plt.show()

# Question 7: Which BHK configuration is most expensive based on per sqft rate?
most_expensive_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax() # Get the BHK configuration with the highest average rate per square foot
print(f"The most expensive BHK configuration on average is {most_expensive_bhk} BHK.")

# Question 8: Which property type is the costliest?
most_expensive_property_type = df.groupby('flat_type')['rate_per_sqft'].mean().idxmax() # Get the property type with the highest average rate per square foot
print(f"The most expensive property type is {most_expensive_property_type}.")

# Question 9: Do certain builders price higher?
# print(df.groupby("company_name")["rate_per_sqft"].mean().sort_values(ascending=False).head(5)) # Print the average rate per square foot for each builder, sorted in descending order
# print name of top 5 
print("The top 5 builders that price higher are:", end=" ") 
top_5_builders = df.groupby("company_name")["rate_per_sqft"].mean().sort_values(ascending=False).head(5)
for builder in top_5_builders.index:
    print(builder, end=", ") # Print the names of the top 5 builders

# Question 10: Are larger homes more expensive per sqft?
sns.scatterplot(data=df, x='area', y='rate_per_sqft') # Create a scatter plot of area vs. rate per square foot
plt.show()
import pandas as pd

# Load the dataset from the provided CSV file path
data = pd.read_csv('data/test.csv')

# Group by 'meta_employer' to find the maximum value of 'itemized_contributions' for each
agg_data = data.groupby(['meta_employer'])['itemized_contributions'].max().reset_index()

# Sort by the maximum contributions descending to find the top contributors
agg_data = agg_data.sort_values(by='itemized_contributions', ascending=False)

# Limit to 5-8 results to avoid overcrowding visualization charts
agg_data = agg_data.head(8)

# Save the transformed data to the given CSV file path
agg_data.to_csv('data/transformed_0.csv', index=False)

print("Transformation complete and saved to 'data/transformed_0.csv'.")
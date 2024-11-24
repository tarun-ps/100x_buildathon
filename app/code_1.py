import pandas as pd

# Load data from CSV file
data_path = 'data/test.csv'
data = pd.read_csv(data_path)

# Aggregate data by 'meta_employer' and calculate summed amounts
aggregated_data = data.groupby('meta_employer')['sum_max_agg'].sum().reset_index()

# Sort the data to find meta_employers with the highest summed amount
aggregated_data_sorted = aggregated_data.sort_values(by='sum_max_agg', ascending=False)

# Limit to the top 5 meta_employers
filtered_data = aggregated_data_sorted.head(5)

# Save the transformed data to a new CSV file
output_path = 'data/transformed_1.csv'
filtered_data.to_csv(output_path, index=False)

# Display the output data
print(filtered_data)
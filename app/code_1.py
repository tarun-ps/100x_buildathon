import pandas as pd

# Load the dataset from the csv file
data = pd.read_csv('data/test.csv')

# Aggregate contributions by committee
total_contributions = data.groupby('committee', as_index=False)['sum_max_agg'].sum()

# Sort the committees by total contributions in descending order and select the top 5-8 committees
sorted_contributions = total_contributions.sort_values(by='sum_max_agg', ascending=False).head(8)

# Save the transformed DataFrame to a new CSV file
sorted_contributions.to_csv('data/transformed_1.csv', index=False)
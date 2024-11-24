import pandas as pd

# Load the dataset
data = pd.read_csv('data/test.csv')

# Group data by 'committee' and calculate the total contributions from both metrics
aggregation = data.groupby('committee')[['itemized_contributions', 'sum_max_agg']].sum()

# Sort values by the sum of both metrics to find most contributing committees
top_committees = aggregation.sum(axis=1).nlargest(8).index

# Filter the data to include only the top committees
data_filtered = aggregation.loc[top_committees]

# Sort for presentation clarity
data_filtered = data_filtered.sort_values(by='sum_max_agg', ascending=False).reset_index()

# Save the transformed data
data_filtered.to_csv('data/transformed_3.csv', index=False)
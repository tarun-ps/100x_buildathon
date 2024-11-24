import pandas as pd

# Load the data from the provided CSV
input_filepath = 'data/test.csv'
data = pd.read_csv(input_filepath)

# Aggregate the contributions by 'meta_employer' across all 'committee'
aggregated_data = data.groupby('meta_employer').agg({
    'itemized_contributions': 'mean'
}).reset_index()

# Rename columns to merge categories and sort by contribution mean
aggregated_data = aggregated_data.rename(columns={
    'meta_employer': 'employer',
    'itemized_contributions': 'average_itemized_contribution'
})

# Sort by average contribution and limit to top 8
aggregated_data = aggregated_data.sort_values(by='average_itemized_contribution', ascending=False).head(8)

# Save the transformed data to a new CSV
output_filepath = 'data/transformed_0.csv'
aggregated_data.to_csv(output_filepath, index=False)
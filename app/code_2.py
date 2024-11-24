import pandas as pd

# Load the dataset
data_path = 'data/test.csv'
df = pd.read_csv(data_path)

# Compute the average itemized contribution per 'meta_employer' and 'committee'
avg_df = df.groupby(['meta_employer', 'committee'], as_index=False)['itemized_contributions'].mean()

# Pivot the dataframe to have committees as the columns for value comparison
pivot_df = avg_df.pivot(index='meta_employer', columns='committee', values='itemized_contributions')

# Select top 5 meta_employers based on average contribution across committees
pivot_df['average_contribution'] = pivot_df.mean(axis=1)
pivot_df = pivot_df.nlargest(5, 'average_contribution').drop(columns=['average_contribution'])

# Reset Index
transformed_df = pivot_df.reset_index()

# Save the resulting dataframe to a new CSV file
output_path = 'data/transformed_2.csv'
transformed_df.to_csv(output_path, index=False)
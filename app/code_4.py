import pandas as pd

# Load the data from the CSV file
data_path = 'data/test.csv'
df = pd.read_csv(data_path)

# Group data by 'committee' and extract unique meta_employers associated with them
committee_meta_employer_counts = df.groupby('committee')['meta_employer'].nunique()

# Filter committees that have contributions from only one meta_employer
single_meta_employer_committees = committee_meta_employer_counts[committee_meta_employer_counts == 1].index

# Filter the dataframe to include only these committees
filtered_df = df[df['committee'].isin(single_meta_employer_committees)]

# Combine 'committee' and 'meta_employer' columns into a single label column
filtered_df['label'] = filtered_df['committee'] + ' - ' + filtered_df['meta_employer']

# Select and rename columns to include label and value columns
result_df = filtered_df[['label', 'itemized_contributions', 'sum_max_agg']]

# To avoid overcrowding in the visualization, limit to Top 5 highest 'sum_max_agg'
result_df = result_df.nlargest(5, 'sum_max_agg')

# Save the transformed data to a new CSV file
save_path = 'data/transformed_4.csv'
result_df.to_csv(save_path, index=False)
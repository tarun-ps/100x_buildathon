import pandas as pd

# Load the dataset
data = pd.read_csv('data/test.csv')

# Establish the threshold for exclusive contributions
t = 100000

# Group the data by committees
committee_groups = data.groupby('committee').agg({
    'itemized_contributions': ['mean', 'min', 'max'],
    'sum_max_agg': ['mean']
})
committee_groups.columns = ['itemized_contributions_mean', 'itemized_contributions_min', 'itemized_contributions_max', 'sum_max_agg_mean']
committee_groups.reset_index(inplace=True)

# Filter committees exclusively above or below the threshold
above_threshold = committee_groups[committee_groups['itemized_contributions_min'] > t]
below_threshold = committee_groups[committee_groups['itemized_contributions_max'] < t]

# Combine the results and choose the top 5 by 'sum_max_agg_mean'
relevant_committees = pd.concat([above_threshold, below_threshold]).nlargest(5, 'sum_max_agg_mean')

# Select columns suitable for the question: 'committee' as the label and summaries as values
transformed_data = relevant_committees[['committee', 'itemized_contributions_mean', 'sum_max_agg_mean']]

# Save the transformed dataframe to a csv
transformed_data.to_csv('data/transformed_4.csv', index=False)
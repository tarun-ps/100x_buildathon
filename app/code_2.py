import pandas as pd

# Load the dataset
data_path = 'data/test.csv'
df = pd.read_csv(data_path)

# Sum contributions by employer
df_grouped = df.groupby('meta_employer')[['itemized_contributions', 'sum_max_agg']].sum()

# Identify the top two employers by total contributions
top_employers = df_grouped.nlargest(2, 'sum_max_agg')

# Filter data for the top two employers
df_top = df[df['meta_employer'].isin(top_employers.index)]

# Combine category columns (if applicable)
df_top['label'] = df_top['meta_employer'] + ' - ' + df_top['committee']

# Group by 'label' for visualization purposes
df_transformed = df_top.groupby('label')[['itemized_contributions', 'sum_max_agg']].sum().reset_index()

# Save the transformed dataframe
output_path = 'data/transformed_2.csv'
df_transformed.to_csv(output_path, index=False)

print("Transformed dataframe saved to:", output_path)
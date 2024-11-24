import pandas as pd

# Load the data
data_path = 'data/test.csv'
df = pd.read_csv(data_path)

# Calculate the standard deviation of contributions within each employer across committees
df_std = df.groupby('meta_employer')['itemized_contributions'].std().reset_index()
df_std = df_std.rename(columns={'itemized_contributions': 'std_contributions'})

# Sort by standard deviation (largest first) and limit to top 5-8 rows
max_records = 8
df_std = df_std.sort_values(by='std_contributions', ascending=False).head(max_records)

# Save the transformed dataframe
df_std.to_csv('data/transformed_3.csv', index=False)

print("Transformation complete. Data saved to 'data/transformed_3.csv'.")
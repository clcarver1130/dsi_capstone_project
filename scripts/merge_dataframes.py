# Load libraries
import pandas as pd

print('Loading data...')
# Load in labeled data: df_labeled
df_labeled = pd.read_csv('../raw_data/kiva_scraping.csv')

# Load in unlabeled data: df_unlabel
df_unlabel = pd.read_csv('../raw_data/loans.csv')

# Pull out just the 2010 data. Save it to a CSV: df_2010
df_2010 = df_labeled[df_labeled['Funded Date.year'] == 2010]
df_2010.to_csv('..data/df_2010.csv')

print('Merging dataframes...')
# Merge the datasets
df_merged = df_2010.merge(df_unlabel, how='inner', left_on='id', right_on='LOAN_ID')
df_merged.to_csv('..data/merged_df.csv')

print("Done. 'df_2010' and 'df_merged' saved to data directory")

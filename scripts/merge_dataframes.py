# Load libraries
import pandas as pd
import boto

# Connect to s3 bucket: clcarver.kiva
conn = boto.connect_s3()
bucket = conn.get_bucket('clcarverloans')

print('Loading data...')
# Load in labeled data: df_labeled
df_labeled = pd.read_csv('../raw_data/kiva_scraping.csv')

# Load in unlabeled data: df_unlabel
df_unlabel = pd.read_csv('../raw_data/loans.csv')

# Pull out just the 2010 data. Save it to a CSV: df_2010
df_2010 = df_labeled[df_labeled['Funded Date.year'] == 2010]
file_2010 = df_2010.to_csv(None)
file_2010 = bucket.new_key('df_2010.csv')
file_2010.set_contents_from_string(file_2010)
print('df_2010 saved to s3')

print('Merging dataframes...')
# Merge the datasets
df_merged = df_2010.merge(df_unlabel, how='inner', left_on='id', right_on='LOAN_ID')
file_merge = df_merged.to_csv(None)
file_merge = bucket.new_key('df_merged.csv')
file_merge.set_contents_from_string(file_merge)
print('df_merged saved to s3')

print('Script Complete')

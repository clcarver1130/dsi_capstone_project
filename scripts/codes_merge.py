# Import libraries
import pandas as pd
import boto
import numpy as np
from config import key, secret_key

# Connect to s3 bucket: clcarver.kiva
conn = boto.connect_s3(key, secret_key)
bucket = conn.get_bucket('clcarverloans')

print('Loading Data...')
df_codes = pd.read_csv('../country_codes.csv')
df_cluster = pd.read_csv('https://s3.amazonaws.com/clcarverloans/data/df_cleaned.csv')

print('Merging Dataframes...')
df_plotly = df_codes.merge(df_cluster, how='inner', left_on='Code_2', right_on='Country Code')
df_plotly.dropna(inplace=True)

print('Saving Dataframe to S3...')
string_plotly = df_plotly.to_csv(None)
file_plotly = bucket.new_key('data/df_plotly.csv')
file_plotly.set_contents_from_string(string_plotly)


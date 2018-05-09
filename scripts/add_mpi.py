# Import libraries
import pandas as pd
import boto
import numpy as np
from config import key, secret_key

# Connect to s3 bucket: clcarver.kiva
conn = boto.connect_s3(key, secret_key)
bucket = conn.get_bucket('clcarverloans')

print('Loading Data...')
df_mpi = pd.read_csv('../mpi_indicators.csv')
df_cluster = pd.read_csv('https://s3.amazonaws.com/clcarverloans/data/df_cluster.csv')

print('Cleaning dataframe...')
df_mpi = df_mpi.replace('..', np.NaN)

print('Merging Dataframes...')
df_plus_economics = df_cluster.merge(df_mpi, how='inner', left_on='Country', right_on='Country')
df_plus_economics.dropna(inplace=True)

print('Saving Dataframe to S3...')
string_economics = df_plus_economics.to_csv(None)
file_economics = bucket.new_key('data/df_indicators.csv')
file_economics.set_contents_from_string(string_economics)

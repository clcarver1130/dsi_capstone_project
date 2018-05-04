# Import libraries
import pandas as pd
import boto
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


# Connect to s3 bucket: clcarver.kiva
conn = boto.connect_s3('SECRET KEYS')
bucket = conn.get_bucket('clcarverloans')

print('Loading data...')
# Load in merged data: df_merged
df_merged = pd.read_csv('https://s3.amazonaws.com/clcarverloans/data/df_merged.csv')

# Select loan 'Use' column: loan_use
loan_use = df_merged['Use'].dropna() # Drop the one missing 'Use' datapoint

print('Vectorizing Description...')
# Create vectorizor and fit_transfrom 'loan_use': vectorizor, x
vectorizer = TfidfVectorizer(stop_words='english')
x = vectorizer.fit_transform(loan_use)

print('Clustering Decriptions...')
# Cluster vectorized descriptions: km
clusters = 8
km = KMeans(n_clusters=8)
km.fit(x)

# Merged Clusters into df_merged: df_cluster
df_cluster = pd.concat([df_merged, pd.DataFrame({'Cluster': km.labels_})], axis=1)
df_cluster.drop(columns='Unnamed: 0', inplace=True) # Drop extra index column
print('New dataframe created')

# Save to s3: df_cluster.csv
string_cluster = df_cluster.to_csv(None)
file_cluster = bucket.new_key('df_cluster.csv')
file_cluster.set_contents_from_string(string_cluster)
print("File 'df_cluster' saved to s3")

print('Script Complete')



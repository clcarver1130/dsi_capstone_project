# Load libraries
import pandas as pd
import boto

print('Loading data...')
# Load in dataframe: df
df = pd.read_csv('https://s3.amazonaws.com/clcarverloans/df_merged.csv')
print('Data loaded')

# Pull columns to keep: col
col = ['id','Funded Date','BORROWER_GENDERS', 'Country Code', 'Country', 'TOWN_NAME', 'Loan Amount','LENDER_TERM','REPAYMENT_INTERVAL','DISTRIBUTION_MODEL','Sector', 'Activity', 'Use', 'Delinquent']
df_select = df[col]

# Reanme columns
df_rename =  df_select.rename(columns=str.title)

# Replace values such as "woman, woman, woman, man" with "group"
df_rename['Borrower_Genders'] = [
    elem if elem in ['female','male'] else 'group' for elem in df_rename['Borrower_Genders']]

print('Data cleaned')


# Connect to s3 bucket: clcarver.kiva
conn = boto.connect_s3('SECRET KEYS')
bucket = conn.get_bucket('clcarverloans')
print('Connected to s3 bucket...')

# Save cleaned dataframe to s3: df_cleaned
string_clean = df_rename.to_csv(None)
file_clean = bucket.new_key('df_cleaned.csv')
file_clean.set_contents_from_string(string_clean)
print("File 'df_cleaned' saved to s3")

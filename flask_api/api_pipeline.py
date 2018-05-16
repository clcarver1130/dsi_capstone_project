import pandas as pd
import pickle
import numpy as np
import requests
import csv

def predict_default(json):
    # Data from web form is submitted: df
    df = pd.DataFrame(json.to_dict(flat=False))
    df.drop(columns='button', inplace=True)

    # 'Loan Use' text is processed and its predicted cluster is added to df
    with open('../scripts/cluster_model.pkl', 'rb') as input:
        cluster_model = pickle.load(input)

    with open('../scripts/vectorizer.pkl', 'rb') as input:
        vectorizer = pickle.load(input)

    use = vectorizer.transform(df['Use'])
    cluster = cluster_model.predict(use)[0]
    df['Cluster'] = cluster
    df.drop(columns='Use', inplace=True)

    # Dummify form submission: df_dummies
    df_dummies = pd.get_dummies(df)

    # Read in list of columns from trained model: full_dummies
    with open('../data/full_col.csv', 'r') as f:
        reader = csv.reader(f)
        full_dummies = list(reader)

    # Add in missing cols with a value of zero to df_dummies: final_df
    missing_cols = set(full_dummies[0]) - set(df_dummies.columns.values)
    for c in missing_cols:
        df_dummies[c] = 0
    final_df = df_dummies[full_dummies[0]]
    final_df.drop(columns='Delinquent', inplace=True)

    # Unpack our model
    with open('../scripts/final_model.pkl', 'rb') as input:
        model = pickle.load(input)
        pred = model.predict_proba(final_df)[:, 1]
        pred_str = str(round(pred[0] * 100, 2)) + '%'

    return pred_str

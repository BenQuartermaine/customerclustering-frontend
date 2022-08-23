import streamlit as st
import requests
import pandas as pd

df = pd.read_csv('raw_data/td.csv', index_col = [0])

'''
# Customerclustering frontend
'''

user_id = st.text_input('Search User ID')

# Hard coded

# user_ids = ['6e6b0e01-4a29-4724-a781-5d6a0d72a213', '6037d38d-d098-4f68-be8c-49b7131b8116']
user_ids = user_id.replace(' ', '').split(',')
print("###########", user_ids)
df_filtered = df[df['userID'].isin(user_ids)]


if len(df_filtered) > 0:
    params = { key: list(val.fillna('*')) for key, val in dict(df_filtered).items() }
    req = dict(passengers = params)

    url = "http://localhost:3001/predict"
    prediction = requests.post(url, json = req).json()
    prediction
else:
    '''
    Waiting waiting
    '''

'''
1. Create docker file, include all the things you need and the path to the raw data
2. Cmd will be running streamlit

'''



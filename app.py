import streamlit as st
import requests
import pandas as pd

st.set_page_config(
            page_title="Customer Clustering", 
            page_icon="👯‍♀️",
            layout="centered")

@st.cache
def get_data():
    df = pd.read_csv('raw_data/td.csv', index_col = [0])
    return df

df = get_data()

'''
## Cluster Overview
Compare how cluster means compare to each other
'''


'''
## Clusters Comparison
View how clusters compare to each other
'''

clusters = ['Cluster 1', 'Cluster 2', 'Cluster  3', 'Cluster 4']
columns = st.columns(len(clusters))

for i, cluster in enumerate(clusters):
    columns[i].checkbox(cluster)

def get_features():
    features = ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4']
    return features

features = get_features()
select_cols = st.columns(2)
x = select_cols[0].selectbox(f'Select x feature', features)
y = select_cols[1].selectbox(f'Select y feature', features)



'''
## Individual Cluster
View how users within a cluster compare to each other
'''
individual_cols = st.columns(3)
# individual_cols[0].radio('Select a cluster', clusters)
clust_ind = individual_cols[0].selectbox(f'Select Cluster', clusters)
x_ind = individual_cols[1].selectbox(f'Select x feature', features, key = [1])
y_ind = individual_cols[2].selectbox(f'Select y feature', features, key = [2])


'''
## Search Individual User(s)
Search for an individual user or set of users to get back what cluster they are a part of
'''

get_user_ids = st.text_input('Search User ID', "Enter one or more user IDs seperated by commas")
# user_ids = ['6e6b0e01-4a29-4724-a781-5d6a0d72a213', '6037d38d-d098-4f68-be8c-49b7131b8116']
user_ids = get_user_ids.replace(' ', '').split(',')
print("###########", user_ids, "###########",)
df_filtered = df[df['userID'].isin(user_ids)]


if len(df_filtered) > 0:
    params = { key: list(val.fillna('*')) for key, val in dict(df_filtered).items() }
    req = dict(passengers = params)

    url = "http://localhost:3001/predict"
    prediction = requests.post(url, json = req).json()
    prediction
else:
    '''
    Enter a valid user ID to see what cluster they are a part of
    '''



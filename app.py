import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from customerclustering_frontend.viz import *
from customerclustering_frontend.check_password import check_password
from customerclustering_frontend.styles import card_style, margin_bottom, line_style, margin_y
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Clustering", page_icon="👯‍♀️",layout="centered")


st.session_state["password"] = ''
load_dotenv(find_dotenv())
app_password = os.environ.get("APP_PASSWORD")

if check_password(app_password):
    print("########################## #######################")

    @st.cache(allow_output_mutation=True)
    def get_data():
        df = pd.read_csv('raw_data/pca.csv', index_col=[0])
        return df

    df = get_data()
    df_viz = GetViz(df)
    print("THIS IS VIZ##############", df_viz.cluster_df, df_viz.feature_df)
    
    #   important columns
    important_columns = ['minPerYear', 
                         'GoalsPerYear', 
                        #  'account_age',
                         'numQueuedPerYear', 
                         'minCompletedOnelinePerYear', 
                         'docOnAusmedPerYear',
                         'learnFromAusmedRatio_min', 
                         'subscribe_days']

    
    df_means = df_viz.get_Kmeans().loc[important_columns]
    print(df_means)

    clusters = df_means.columns
    '''
    ## Cluster Overview
    Compare how cluster means compare to each other
    '''

    mean_top_columns = st.columns(3)

    for index, (key, value) in enumerate(df_means.loc[:, :clusters[2]].items()):
        mean_top_columns[index].write(f"<style>{margin_bottom}</style><h4>{key}</h4>", unsafe_allow_html=True)

        for k, v in value.items():
            item = f'<style>{line_style}</style><div class="line"><div>{k}</div><div>{v}</div></div>'
            mean_top_columns[index].write(item, unsafe_allow_html=True)

    mean_bottom_columns = st.columns(3)

    count = 0
    for index, (key, value) in enumerate(df_means.loc[:, clusters[3]:clusters[5]].items()):
        mean_bottom_columns[count].write(f"<style>{margin_y} </style><h4>{key}</h4>", unsafe_allow_html=True)
        for k, v in value.items():
            item = f'<style>{line_style}</style><div class="line"><div>{k}</div><div>{v}</div></div>'
            mean_bottom_columns[count].write(item, unsafe_allow_html=True)
        count += 1


    '''
    ## Clusters Comparison
    View how clusters compare to each other
    '''


    features = df.columns

    x = st.selectbox(f'Select a feature', important_columns)
    fig = df_viz.clusters_one_feature(x)
    print('##############', "Feature 1 preparing plot")
    st.pyplot(fig)
    print('##############', "Feature 1 Plot prepared")


    '''
    ## Individual Cluster
    View how users within a cluster compare to each other
    '''
    individual_cols = st.columns(3)
    clust_ind = individual_cols[0].selectbox(f'Select Cluster', clusters)
    x_ind = individual_cols[1].selectbox(f'Select x feature', important_columns, key = [1])
    y_ind = individual_cols[2].selectbox(f'Select y feature', important_columns, key = [2])

    fig, ax = plt.subplots()
    fig = df_viz.cluster_two_feature(clust_ind, x_ind, y_ind)
    print('##############', "Preparing plot")
    st.pyplot(fig)
    print('##############', "Plot prepared")



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
else:
    '''Nope ❌'''

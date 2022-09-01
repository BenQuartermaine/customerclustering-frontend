import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from customerclustering_frontend.viz import *
from customerclustering_frontend.check_password import check_password
from customerclustering_frontend.styles import card_style, margin_bottom, line_style, margin_y
import matplotlib.pyplot as plt


st.set_page_config(page_title="Customer Clustering", page_icon="👯‍♀️",layout="wide")

load_dotenv(find_dotenv())
app_password = os.environ.get("APP_PASSWORD")


if check_password(app_password):
    print("########################## #######################")

    @st.cache
    def get_data():
        df = pd.read_csv('raw_data/pca.csv')
        return df

    @st.cache
    def get_Viz_data(df):
        return GetViz(df)

    df = get_data()
    viz = get_Viz_data(df.sample(200))

    df_means = viz.get_Kmeans()
    # df_means = df_means.loc[['account_age', 'docPerYear', 'docOnAusmedPerYear', 'subscribe_days', 'minPerYear', 'numCompletedFromQueue', 'minCompletedFromQueue', 'activated']]


    clusters = list(df_means.columns)
    print("##########################",clusters, "#######################")
    '''
    ## Cluster Overview
    Compare how cluster means compare to each other
    '''

    mean_top_columns = st.columns(3)

    for index, (key, value) in enumerate(df_means.loc[:, :clusters[2]].items()):

        # mean_columns[index].write(f"<style>{card_style}</style><div class='card'>{key}</div>", unsafe_allow_html=True)
        mean_top_columns[index].write(f"<style>{margin_bottom}</style><h4>{key}</h4>", unsafe_allow_html=True)

        for k, v in value.items():
            item = f'<style>{line_style}</style><div class="line"><div>{k}</div><div>{v}</div></div>'
            mean_top_columns[index].write(item, unsafe_allow_html=True)

    mean_bottom_columns = st.columns(3)

    count = 0
    for index, (key, value) in enumerate(df_means.loc[:, clusters[3]:clusters[5]].items()):
        # mean_columns[index].write(f"<style>{card_style}</style><div class='card'>{key}</div>", unsafe_allow_html=True)
        mean_bottom_columns[count].write(f"<style>{margin_y} </style><h4>{key}</h4>", unsafe_allow_html=True)
        for k, v in value.items():
            item = f'<style>{line_style}</style><div class="line"><div>{k}</div><div>{v}</div></div>'
            mean_bottom_columns[count].write(item, unsafe_allow_html=True)
        count += 1


    '''
    ## Clusters Comparison
    View how clusters compare to each other
    '''


    # take in the feature name


    # write the plot to the file

    def get_features(df):
        features = df.columns
        return features
    features = get_features(df)

    x = st.selectbox(f'Select a feature', features)
    @st.cache
    def get_clusters_one_feature():
        # fig, ax = plt.subplots()
        fig = viz.clusters_one_feature(x)
        print('##############', "Feature 1 preparing plot")
        return fig
    fig = get_clusters_one_feature()
    st.pyplot(fig)
    print('##############', "Feature 1 Plot prepared")


    '''
    ## Individual Cluster
    View how users within a cluster compare to each other
    '''
    individual_cols = st.columns(3)
    clust_ind = individual_cols[0].selectbox(f'Select Cluster', clusters)
    x_ind = individual_cols[1].selectbox(f'Select x feature', features, key = [1])
    y_ind = individual_cols[2].selectbox(f'Select y feature', features, key = [2])

    fig, ax = plt.subplots()
    two_plot = viz.cluster_two_feature(clust_ind, x_ind, y_ind)
    print('##############', "Preparing plot")
    st.pyplot(fig)
    print('##############', "Plot prepared")



    '''
    ## Search Individual User(s)
    Search for an individual user or set of users to get back what cluster they are a part of
    '''

    get_user_ids = st.text_input('Search User ID', "Enter one or more user IDs seperated by commas")
    # user_ids = ['6e6b0e01-4a29-4724-a781-5d6a0d72a213', '6037d38d-d098-4f68-be8c-49b7131b8116']
    # user_ids = get_user_ids.replace(' ', '').split(',')
    # print("###########", user_ids, "###########",)
    # df_filtered = df[df['userID'].isin(user_ids)]


    # if len(df_filtered) > 0:
    #     params = { key: list(val.fillna('*')) for key, val in dict(df_filtered).items() }
    #     req = dict(passengers = params)

    #     url = "http://localhost:3001/predict"
    #     prediction = requests.post(url, json = req).json()
    #     prediction
    # else:
    #     '''
    #     Enter a valid user ID to see what cluster they are a part of
    #     '''
else:
    '''Nope ❌'''

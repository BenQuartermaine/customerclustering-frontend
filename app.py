from multiprocessing.spawn import import_main_path
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

    @st.cache(allow_output_mutation=True)
    def get_data():
        df = pd.read_csv('raw_data/pca.csv', index_col=[0])
        return df

    df = get_data()
    df_viz = GetViz(df)
    
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
    ## Search Individual User
    Search for an individual user or set of users to get back what cluster they are a part of
    '''
    
    imp_cols = ['minPerYear', 
                'GoalsPerYear', 
                #  'account_age',
                'numQueuedPerYear', 
                'minCompletedOnelinePerYear', 
                'docOnAusmedPerYear',
                'learnFromAusmedRatio_min', 
                'subscribe_days', 'cluster_id', 'userID']

    get_user_ids = st.text_input('Search User ID')
    # user_ids = ['06c50aef-c911-4efb-baf0-73aab6d64aaa', '6037d38d-d098-4f68-be8c-49b7131b8116']
    user_ids = get_user_ids.replace(' ', '').split(',')
    print("###########", user_ids, "###########",)
    df_filtered = df[df['userID'].isin(user_ids)]
    individual_cluster_id = df_filtered.iloc[0]['cluster_id']
    df_filt_important = round(df_filtered[imp_cols], 2).transpose()
    header_row = df_filt_important.loc['userID']
    df_filt_important.columns = header_row
    
    print(df_means.loc[:, clusters[individual_cluster_id]])
    
    if len(df_filtered) > 0:
        individual_user_cols = st.columns(2)
      
        for index, (key, value) in enumerate(df_filt_important.items()):
            individual_user_cols[0].write(f"<style>{margin_bottom}</style><h4>User</h4>", unsafe_allow_html=True)

            for k, v in value.items():
                item = f'<style>{line_style}</style><div class="line"><div>{k}</div><div>{v}</div></div>'
                individual_user_cols[0].write(item, unsafe_allow_html=True)
        
            individual_user_cols[1].write(f"<style>{margin_bottom}</style><h4>Cluster {individual_cluster_id}</h4>", unsafe_allow_html=True)
        for key, value in enumerate(df_means.loc[:, clusters[individual_cluster_id]].items()):
            item = f'<style>{line_style}</style><div class="line"><div>{value[0]}</div><div>{value[1]}</div></div>'
            individual_user_cols[1].write(item, unsafe_allow_html=True)

            # for k, v in value.items():


        # params = { key: list(val.fillna('*')) for key, val in dict(df_filtered).items() }
        # req = dict(passengers = params)

        # url = "http://asia.gcr.io/wagon-le-8888/customerclustering-api/predict"
        # prediction = requests.post(url, json = req).json()
    else:
        '''
        Enter a valid user ID to see what cluster they are a part of
        '''
else:
    '''Nope ❌'''

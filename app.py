import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv


st.set_page_config(
            page_title="Customer Clustering", 
            page_icon="👯‍♀️",
            layout="centered")

load_dotenv(find_dotenv())
app_password = os.environ.get("APP_PASSWORD")

st.session_state["password"] = ''
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == app_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    @st.cache
    def get_data():
        df = pd.read_csv('raw_data/td.csv', index_col = [0])
        return df

    df = get_data()

    clusters = ['cluster 1', 'cluster 2', 'cluster  3', 'cluster 4']

    cluster_means = {
        'cluster 1': {
            'feature_1': 10,
            'feature_2': 'Rural',
            'feature_3': 8.3
        },
        'cluster 2': {
            'feature_1': 3,
            'feature_2': 'Other',
            'feature_3': 98.7
        }
        ,
        'cluster 3': {
            'feature_1': 3,
            'feature_2': 'Other',
            'feature_3': 98.7
        }
    }

    '''
    ## Cluster Overview
    Compare how cluster means compare to each other
    '''
    card_style = """
        .card {
            background: #FFFFFF;
            box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.08);
            border-radius: 24px;
        }
    """
    margin_bottom = """ 
        p { 
            margin-bottom: 8px;
        }
    """
    line_style = """
        .line {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    
    """
    mean_columns = st.columns(len(clusters))
    
    for index, (key, value) in enumerate(cluster_means.items()):
        
        # mean_columns[index].write(f"<style>{card_style}</style><div class='card'>{key}</div>", unsafe_allow_html=True)
        mean_columns[index].write(f"<style>p {margin_bottom}</style><b>{key}</b>", unsafe_allow_html=True)

        for k, v in value.items():
            item = f'<style>{line_style}</style><div class="line"><div>{k}</div><div>{v}</div></div>'
            mean_columns[index].write(item, unsafe_allow_html=True)


    '''
    ## Clusters Comparison
    View how clusters compare to each other
    '''

    comparison_columns = st.columns(len(clusters))
    for i, cluster in enumerate(clusters):
        comparison_columns[i].checkbox(cluster)

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

    # if we store the CSV in the frontend, do we need to do an API call? if we just include a column with cluster?

    # setup password
    # putting CSV in bucket
        # seciton in the lecture
    # pushing to GCP
        # check predict in production
            # docker asia.gcr.io/wagon-le-8888/customerclustering-frontend
        # build run push deploy
        # Push to, run from


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


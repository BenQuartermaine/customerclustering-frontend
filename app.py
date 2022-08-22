import streamlit as st
import requests

'''
# Customerclustering frontend

### TODO
1. Add csv data to frontend repo
2. Take in a user ID
3. Filter the CSV data to get that users features
4. Submit the row(s) to the predict API
5. Display the prediction

### QUESTIONS:
1. If we use a CSV and a new user becomes apart of the data set, how will the aggrgate displays update overtime?
2. On page load, should a predict call happen to be able to display the clusters?
3. How do we set up the mechanism to continuously update the model (is it done by periodically querying the production database and updating the frontend CSV?)
'''

'''
### Test API
'''

url = 'http://localhost:8001/'
resp = requests.get('http://localhost:8001/').json()

if url == 'http://localhost:8001/':

    resp

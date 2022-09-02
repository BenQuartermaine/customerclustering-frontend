import io
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from app import *
from sklearn import set_config; set_config(display='diagram')

class GetViz:
    def __init__(self, df):
        # Import data only once

        self.cluster_df, self.feature_df = self.get_cluster_df(df)
        self.cat_columns, self.num_columns = self.get_feature_cat()

    def get_cluster_df(self,cluster_df):
        # def cluster_transform(x):
        #     return f"cluster {str(int(x)+1)}"

        # get data from the csv file with the label information
        # cluster_df.loc[:,'cluster_id'] = cluster_df['cluster_id'].apply(cluster_transform)
        feature_df = cluster_df.drop(columns=['cluster_id','userID'])
        cluster_df['count'] = 1
        return cluster_df, feature_df

    def get_feature_cat(self):

        #getting date types from feature dataframe
        buffer = io.StringIO()
        self.feature_df.info(buf=buffer)
        lines = buffer.getvalue().splitlines()
        column_df = (pd.DataFrame([x.split() for x in lines[6:-2]], columns=lines[3].split())
            .drop('Count',axis=1)
            .rename(columns={'Non-Null':'Non-Null Count'}))

        #getting num and cat features
        cat_columns = column_df[column_df['Dtype']=='object'].reset_index().Column
        num_columns = column_df[column_df['Dtype']!='object'].reset_index().Column

        return cat_columns, num_columns


    def get_Kmeans(self):

        #create df for different feature categories to help with visualisation
        num_features_df = self.cluster_df[self.num_columns]
        num_features_df['cluster_id'] = self.cluster_df['cluster_id']

        cat_features_df = self.cluster_df[self.cat_columns]
        cat_features_df['cluster_id'] = self.cluster_df['cluster_id']

        #calculate and consolidate all kmeans in one dataframe
        num_kmean_df = round(num_features_df.groupby('cluster_id').mean().transpose(), 2)
        cat_kmean_df = cat_features_df.groupby('cluster_id')[self.cat_columns].agg(pd.Series.mode).transpose()
        kmean_df = num_kmean_df.append(cat_kmean_df)
        return kmean_df

    def clusters_one_feature(self, feature):

        #viz for num features using boxplot

        if feature in list(self.num_columns):
            print("boxplot is running")
            fig, ax = plt.subplots(figsize = (3,3) )
            sns.boxplot(x = 'cluster_id', y = feature, hue = 'cluster_id', \
                data = self.cluster_df.sample(200), palette='bright', ax=ax)

            return fig

        #viz for cat features using heatmap
        else:
            print("heatmap is running")
            fig, ax = plt.subplots(figsize = (3,3) )
            heat_df = pd.pivot_table(self.cluster_df.sample(200), values='count', index=[feature],
                                columns=['cluster_id'], aggfunc=np.sum, fill_value=0)

            for col in heat_df.columns:
                total = heat_df[col].sum()
                heat_df[col] = round(heat_df[col]/total,2)
            sns.heatmap(heat_df, annot = True, ax = ax)

            return fig

    def cluster_two_feature(self,cluster,feature1,feature2):
        '''Returns a scatterplot'''
        fig, ax = plt.subplots(figsize = (3,3) )

        cluster_df_filtered = self.cluster_df[self.cluster_df['cluster_id']== cluster]
        scatter = sns.scatterplot(data = cluster_df_filtered, x = feature1, y = feature2, palette='bright')
        return fig

if __name__ == "__main__":
    df = pd.read_csv('raw_data/pca.csv')
    print(GetViz(df).get_Kmeans())

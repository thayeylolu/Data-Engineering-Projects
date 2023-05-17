# importing libaries

import os
import boto3
import pandas as pd
import s3fs
import numpy as np
import sagemaker as sg
import seaborn as sns
import datetime as dt
import geopy.distance
import matplotlib.pyplot as plt
import warnings

from statsmodels.formula import api
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from IPython.display import display
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

plt.rcParams['figure.figsize'] = [10,6]
warnings.filterwarnings('ignore')

# aws role and region
role = sg.get_execution_role()
region = boto3.Session().region_name

# print(region)
# print(role)

# read data from s3
bucket = "ml-data-sceince-bucket"
prefix = "uberfare"
filename = "uber.csv"

data_s3_location = "s3://{}/{}/{}".format(bucket, prefix, filename)  # S3 URL
df = pd.read_csv(data_s3_location)
# df.head()

# drop unnamed column
df.drop(['Unnamed: 0','key'], axis=1, inplace=True)
display(df.head())

target = 'fare_amount'
features = [i for i in df.columns if i not in [target]]

# print('\n Descriptive: The Datset consists of {} features & {} samples.'.format(df.shape[1], df.shape[0]))

# lat -90 to 90 and long -180 to 180
s = df[(df.pickup_latitude<=90) & (df.dropoff_latitude<=90) &
        (df.pickup_latitude>= -90) & (df.dropoff_latitude>= -90) &
        (df.pickup_longitude<= 180) & (df.dropoff_longitude<= 180) &
        (df.pickup_longitude>= -180) & (df.dropoff_longitude>= -180)]
# s.info()

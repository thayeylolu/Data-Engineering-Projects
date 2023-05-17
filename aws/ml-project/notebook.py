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


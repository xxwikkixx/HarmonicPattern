import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

# Importing Data
data = pd.read_csv('file.csv')
data.columns  = [['Data', 'Open', 'High', 'Low', 'Close', 'Vol']]
data = data.drop_duplicates(keep=False)
data.Date = pd.to_datetime(data.Date, format='%d.%m.%Y %H:%M:%S.%f')
data = data.set_index(data.Date)
data = data[['Open', 'High', 'Low', 'Close', 'Vol']]
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

# Importing Data
data = pd.read_csv('file.csv')
data.columns = [['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
data.Date = pd.to_datetime(data.Date, format='%d.%m.%Y %H:%M:%S.%f')
data = data.set_index(data.Date)
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data = data.drop_duplicates(keep=False)

# Select set of the data, first 100 points
price = data.Close.iloc[:1000]

# Find peaks
for i in range(100, len(price)):
    # Find our relative extrema
    # Return the max indexes of the extrema
    max_idx = list(argrelextrema(price.values, np.greater, order=10)[0])
    # Return the min indexes of the extrema
    min_idx = list(argrelextrema(price.values, np.less, order=10)[0])
    idx = max_idx + min_idx
    idx.sort()
    current_idx = idx[-5:]

    start = min(current_idx)
    end = max(current_idx)

    current_pat = price.values[current_idx]

    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        plt.plot(np.arange(start, i), price.values[start:i])
        plt.scatter(idx, current_pat, c='r')
        plt.show()
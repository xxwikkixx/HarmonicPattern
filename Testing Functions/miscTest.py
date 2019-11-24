import time
import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from tosdb.intervalize import ohlc
from timeit import default_timer

def plotMaxMin():
    data = pd.read_csv('cltick.csv')
    data['time'] = pd.to_datetime(data['time'], format='%d.%m.%Y %H:%M:%S.%f')
    data = data.set_index(data['time'])
    data = data.drop_duplicates(keep=False)
    price = data['Close']
    price = price.drop_duplicates(keep=False)

    # Finds the maximums index
    max_idx = np.argmax(price.values)
    # Finds the minimums index
    min_idx = np.argmin(price.values)

    SmaOutput = talib.SMA(price, 9)

    print(max_idx)
    print(min_idx)

    plt.title('Close Price')
    # plt.figure(dpi=600)
    plt.plot(price.values)
    
    plt.plot(SmaOutput.values)

    plt.scatter(max_idx, max(price.values), c='r')
    plt.scatter(min_idx, min(price.values), c='r')
    plt.show()


def plotPeaks(price):
    # Find our relative extrema
    # Return the max indexes of the extrema
    max_idx = list(argrelextrema(price, np.greater, order=10)[0])
    # Return the min indexes of the extrema
    min_idx = list(argrelextrema(price, np.less, order=10)[0])
    idx = max_idx + min_idx + [len(price) - 1]
    idx.sort()
    current_idx = idx[-5:]
    start = min(current_idx)
    end = max(current_idx)
    current_pat = price[current_idx]

    plt.title('Close Price')
    plt.figure(dpi=800)
    plt.plot(price.values)
    plt.scatter(current_idx, current_pat, c='r')
    plt.show()

    return current_idx, current_pat, start, end


def supres(ltp, n):
    """
    This function takes a numpy array of last traded price
    and returns a list of support and resistance levels
    respectively. n is the number of entries to be scanned.
    """
    from scipy.signal import savgol_filter as smooth
    # converting n to a nearest even number
    if n % 2 != 0:
        n += 1
    n_ltp = ltp.shape[0]
    # smoothening the curve
    ltp_s = smooth(ltp, (n + 1), 3)
    # taking a simple derivative
    ltp_d = np.zeros(n_ltp)
    ltp_d[1:] = np.subtract(ltp_s[1:], ltp_s[:-1])
    resistance = []
    support = []
    for i in range(n_ltp - n):
        arr_sl = ltp_d[i:(i + n)]
        first = arr_sl[:(n // 2)]  # first half
        last = arr_sl[(n // 2):]  # second half
        r_1 = np.sum(first > 0)
        r_2 = np.sum(last < 0)
        s_1 = np.sum(first < 0)
        s_2 = np.sum(last > 0)
        # local maxima detection
        if (r_1 == (n / 2)) and (r_2 == (n / 2)):
            resistance.append(ltp[i + ((n // 2) - 1)])
        # local minima detection
        if (s_1 == (n / 2)) and (s_2 == (n / 2)):
            support.append(ltp[i + ((n // 2) - 1)])

    return support, resistance

if __name__ == '__main__':
    pass

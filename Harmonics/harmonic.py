import matplotlib.pyplot as plt
from Harmonics.harmonic_func import *

# Importing Data
data = pd.read_csv('file.csv')
data['time'] = pd.to_datetime(data['time'], format='%d.%m.%Y %H:%M:%S.%f')
data = data.set_index(data['time'])
data = data.drop_duplicates(keep=False)
price = data['Close'].copy()

err_allowed = 10.0/100

# Find peaks
for i in range(100, len(price)):
    current_idx, current_pat, start, end = peak_detect(price.values[:i])

    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    moves = [XA, AB, BC, CD]

    gartley = is_Gartley(moves, err_allowed)
    butterfly = is_Butterfly(moves, err_allowed)
    bat = is_Bat(moves, err_allowed)
    crab = is_Crab(moves, err_allowed)

    harmonics = np.array([gartley, butterfly, bat, crab])
    labels = [
        'Gartley',
        'Butterfly',
        'Bat',
        'Crab'
    ]

    if np.any(harmonics == 1) or np.any(harmonics == -1):
        for j in range(0, len(harmonics)):
            if harmonics[j] == 1 or harmonics[j] == -1:
                sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
                label = sense + labels[j] + ' Found'

                plt.title(label)
                plt.plot(np.arange(start, i+15), price.values[start:i+15])
                plt.scatter(current_idx, current_pat, c='r')
                plt.show()

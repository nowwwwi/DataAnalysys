import matplotlib.pyplot as plt
import pandas as pd


def make_scatter(df: pd.DataFrame):
    x, y = df['distance'], df['travel_time']

    plt.scatter(x, y, s=3)

    plt.title('Time and Distance Relationships(Tokyo-Destination)')
    plt.xlabel('Distance[km]')
    plt.ylabel('Time[minute]')
    plt.axvline(x=517.2, color='r')
    plt.axhline(y=163, color='r')

    plt.savefig('figures/scatter.png')

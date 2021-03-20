import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def generate(mapsize, num=5):
    plt.figure(figsize=(mapsize/100, mapsize/100))

    x = np.linspace(5, 10, num, endpoint=True)

    flist = []
    DB = 4
    for i in range(DB):
        y = np.cos(-x ** np.random.rand() * 3 + 3 / np.random.rand() + 10)
        flist.append(interp1d(x, y, kind='nearest'))

    xnew = np.linspace(5, 10, num=2000, endpoint=True)

    for curve in flist:
        plt.plot(xnew, curve(xnew), '-', color='k')

    plt.axis('off')
    plt.grid(False)

    plt.savefig('./data/road_img.png')

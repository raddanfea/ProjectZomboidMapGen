import timeit

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from numpy.random._generator import default_rng
from scipy.interpolate import make_interp_spline


def generate(mapsize):
    plt.figure(figsize=(mapsize / 100, mapsize / 100))

    rivers = range(0, round(mapsize / 3000))
    bendyness = 1
    if len(rivers) == 1 and np.random.rand() < 0.5:
        rivers = [1]

    for i in rivers:
        rng = default_rng()

        x = np.array(sorted(rng.choice(100, size=10, replace=False)))
        y = np.array(sorted(rng.choice(100, size=10, replace=False)))

        xnew = np.linspace(0, mapsize/100, mapsize*10)

        spl = make_interp_spline(x, y, k=1)
        y_smooth = spl(xnew)

        lwidths = []
        for each in xnew:
            if i != 0:
                lwidths.append(np.random.randint(50, 52))
            else:
                lwidths.append(np.random.randint(71, 73))

        for k in range(len(y_smooth)):
            if i % 2 == 0:
                y_smooth[k] = mapsize / 100 - y_smooth[k]
            elif i % 3 == 0:
                xnew[k] = mapsize / 100 - xnew[k]

        plt.scatter(xnew, y_smooth, s=lwidths, color='k')


    plt.axis('off')
    plt.grid(False)

    ax = plt.gca();
    ax.set_xlim(0.0, mapsize / 100);
    ax.set_ylim(mapsize / 100, 0.0);

    plt.tight_layout()
    plt.savefig('./data/river_img.png', pad_inches=0, bbox_inches=None, metadata=None)


if __name__ == '__main__':
    generate(9000)

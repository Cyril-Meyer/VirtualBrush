import random
import time
import numpy as np
import matplotlib.pyplot as plt
from numba import jit, njit


@njit(fastmath=True)
def bresenham(x0, y0, x1, y1):
    """
    This code is very inspired from this source :
    https://github.com/encukou/bresenham
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    rr, cc = [], []
    for x in range(dx + 1):
        rr.append(x0 + x*xx + y*yx)
        cc.append(y0 + x*xy + y*yy)
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy

    return rr, cc


@njit(fastmath=True)
def bezier(x0, y0, x1, y1, x2, y2, n_samples=10):
    p0 = np.array([x0, y0])
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])

    rr = [x0]
    cc = [y0]

    p_old = np.rint(p0).astype(np.int64)

    for t_ in range(1, n_samples+1):
        t = t_/n_samples
        p = np.rint((1-t)*((1-t)*p0 + t*p1) + t*((1-t)*p1 + t*p2)).astype(np.int64)
        tmp_rr, tmp_cc = bresenham(p_old[0], p_old[1], p[0], p[1])
        rr = rr + tmp_rr
        cc = cc + tmp_cc
        p_old = p

    return rr, cc


@njit(fastmath=True)
def bezier_fast(px0, py0, px1, py1, px2, py2, n_samples=10):
    rr = []
    cc = []

    px_old = px0
    py_old = py0

    for t_ in range(1, n_samples+1):
        t = t_/n_samples
        px = round((1-t)*((1-t)*px0 + t*px1) + t*((1-t)*px1 + t*px2))
        py = round((1-t)*((1-t)*py0 + t*py1) + t*((1-t)*py1 + t*py2))

        dx = px - px_old
        dy = py - py_old

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2 * dy - dx
        y = 0

        for x in range(dx + 1):
            rr.append(px_old + x * xx + y * yx)
            cc.append(py_old + x * xy + y * yy)
            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy

        px_old = px
        py_old = py

    return rr, cc


if __name__ == '__main__':
    X = np.zeros((512, 512), dtype=np.uint8)
    rr, cc = bresenham(0, 0, 500, 250)
    X[rr, cc] = 255
    plt.imshow(X)
    plt.show()
    
    X = np.zeros((512, 512), dtype=np.uint8)
    rr, cc = bezier(0, 0, 0, 512, 500, 250, 10)
    X[rr, cc] = 255
    plt.imshow(X)
    plt.show()

    X = np.zeros((512, 512), dtype=np.uint8)
    rr, cc = bezier_fast(0, 0, 0, 512, 500, 250, 10)
    X[rr, cc] = 255
    plt.imshow(X)
    plt.show()

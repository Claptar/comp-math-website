import numpy as np


def f(u, g, m1, m2, l1, l2):
    f = np.zeros(10)
    f[0] = u[4]
    f[1] = u[5]
    f[2] = u[6]
    f[3] = u[7]
    f[4] = u[8] / m1 * 2 * u[0] - u[9] / m1 * 2 * (u[2] - u[0])
    f[5] = -g + u[8] / m1 * 2 * u[1] - u[9] / m1 * 2 * (u[3] - u[1])
    f[6] = u[9] / m2 * 2 * 2 * (u[3] - u[1])
    f[8] = u[0] ** 2 + u[1] ** 2 - l1 ** 2
    f[9] = (u[2] - u[0]) ** 2 + (u[3] - u[1]) ** 2 - l2 ** 2
    return f


def get_D_matrix():
    D = np.eye(10)
    D[8, 8] = 0
    D[9, 9] = 0
    return D


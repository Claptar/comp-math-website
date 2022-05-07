import numpy as np

# Параметры системы
t0, T = 0., 14.16
g = 9.81
l1, l2 = 5., 2.
m1, m2 = 1.0, 0.1


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


def f_u(u, m1, m2):
    f_u = np.zeros((10, 10))
    # Задаются ненулевые компоненты матрицы Якоби
    f_u[0, 4] = 1.
    f_u[1, 5] = 1.
    f_u[2, 6] = 1.
    f_u[3, 7] = 1.
    f_u[4, 0] = u[8] / m1 * 2 + u[9] / m1 * 2
    f_u[4, 2] = -u[9] / m1 * 2
    f_u[4, 8] = 1 / m1 * 2 * u[0]
    f_u[4, 9] = -1 / m1 * 2 * (u[2] - u[0])
    f_u[5, 1] = u[8] / m1 * 2 + u[9] / m1 * 2
    f_u[5, 3] = -u[9] / m1 * 2
    f_u[5, 8] = 1 / m1 * 2 * u[1]
    f_u[5, 9] = -1 / m1 * 2 * (u[3] - u[1])
    f_u[6, 0] = -u[9] / m2 * 2
    f_u[6, 2] = u[9] / m2 * 2
    f_u[6, 9] = 1 / m2 * 2 * (u[2] - u[0])
    f_u[7, 1] = -u[9] / m2 * 2
    f_u[7, 3] = u[9] / m2 * 2
    f_u[7, 9] = 1 / m2 * 2 * (u[3] - u[1])
    f_u[8, 0] = 2 * u[0]
    f_u[8, 1] = 2 * u[1]
    f_u[9, 0] = -2 * (u[2] - u[0])
    f_u[9, 1] = -2 * (u[3] - u[1])
    f_u[9, 2] = 2 * (u[2] - u[0])
    f_u[9, 3] = 2
    return f_u


def get_D_matrix():
    D = np.eye(10)
    D[8, 8] = 0
    D[9, 9] = 0
    return D


def solve_ode(f, fu, M, t0, T, initial_val, alpha=(1 + 1j)/2):
    tau = (T - t0) / M
    t = np.linspace(t0, T, M + 1)
    u = np.zeros((M + 1, 10))
    u[0, :] = initial_val
    for m in range(M):
        w1 = np.linalg.solve(get_D_matrix() - alpha * tau * fu(u[m], m1, m2), f(u[m], g, m1, m2, l1, l2))
        u[m + 1] = u[m] + tau * w1.real



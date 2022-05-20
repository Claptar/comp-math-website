import numpy as np
from matplotlib.pyplot import style, figure, axes
from celluloid import Camera
import matplotlib.pyplot as plt


# Параметры системы
t0, T = 0., 14.16
g = 9.81
XLIM = (-5.5, 5.5)
YLIM = (-8, 1)
M = 2000


def f(u, g, m1, m2, l1, l2):
    f = np.zeros(10)
    f[0] = u[4]
    f[1] = u[5]
    f[2] = u[6]
    f[3] = u[7]
    f[4] = u[8]/m1*2*u[0] - u[9]/m1*2*(u[2] - u[0])
    f[5] = -g + u[8]/m1*2*u[1] - u[9]/m1*2*(u[3] - u[1])
    f[6] = u[9]/m2*2*(u[2] - u[0])
    f[7] = -g + u[9]/m2*2*(u[3] - u[1])
    f[8] = u[0]**2 + u[1]**2 - l1**2
    f[9] = (u[2] - u[0])**2 + (u[3] - u[1])**2 - l2**2
    return f


def fu(u, m1, m2):
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
    f_u[9, 3] = 2 * (u[3] - u[1])
    return f_u


def get_D_matrix():
    D = np.eye(10)
    D[8, 8] = 0
    D[9, 9] = 0
    return D


def solve_ode(f, fu, M, t0, T, masses, lengths, angles, alpha=(1 + 1j)/2):
    tau = (T - t0) / M
    t = np.linspace(t0, T, M + 1)
    u = np.zeros((M + 1, 10))
    m1, m2 = masses
    l1, l2 = lengths
    phi1, phi2 = angles
    u[0, :] = initialize_values(l1=l1, l2=l2, phi1=phi1, phi2=phi2)
    for m in range(M):
        w1 = np.linalg.solve(get_D_matrix() - alpha * tau * fu(u[m], m1, m2), f(u[m], g, m1, m2, l1, l2))
        u[m + 1] = u[m] + tau * w1.real
    return t, u


def initialize_values(l1, l2, phi1, phi2, v1x=0., v1y=0., v2x=0., v2y=0., lambda1=100., lambda2=100.):
    """
    Function that takes length of the pendulums and their angles and returns their coordinates
    :param l1: length of the pendulum 1
    :param l2: length of the pendulum 2
    :param phi1: angle of the pendulum 1
    :param phi2: angle of the pendulum 2
    :return: list of coordinates
    """
    phi1, phi2 = phi1 / 180 * np.pi, phi2 / 180 * np.pi
    x1, y1 = l1 * np.sin(phi1), YLIM[1] - l1 * np.cos(phi1)
    x2, y2 = x1 + l2 * np.sin(phi2), y1 - l2 * np.cos(phi2)
    return x1, y1, x2, y2, v1x, v1y, v2x, v2y, lambda1, lambda2


def get_the_gif(t, u, M):
    style.use('dark_background')
    fig = plt.figure()
    camera = Camera(fig)
    ax = axes(xlim=XLIM, ylim=YLIM)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    for m in range(M + 1):
        ax.plot(0, 0, color="yellow", marker='o', markersize=5)
        ax.plot((-2, 2), (0, 0), '-', color="white")
        # Отрисовка подвеса 1
        ax.plot((0, u[m, 0]), (0, u[m, 1]), color="white")
        # Отрисовка груза 1
        ax.plot(u[m, 0], u[m, 1], color="white", marker='o', markersize=12)
        # Отрисовка подвеса 2
        ax.plot((u[m, 0], u[m, 2]), (u[m, 1], u[m, 3]), color="white")
        # Отрисовка груза 2
        ax.plot(u[m, 2], u[m, 3], color="white", marker='o', markersize=6)
        # Отрисовка следа груза 1
        ax.plot(u[:m, 0], u[:m, 1], '-g', linewidth=1)
        # Отрисовка следа груза 2
        ax.plot(u[:m, 2], u[:m, 3], '-y', linewidth=1)
        if m % 2 == 0:
            camera.snap()

    tau = t[1] - t[0]
    animation = camera.animate(interval=tau * 1e3, blit=True)
    animation.save('celluloid.gif')


def solve_celluloid_problem(masses, lengths):
    t, u = solve_ode(f, fu, M, t0, T, masses, lengths, alpha=(1 + 1j)/2)
    get_the_gif(t, u, M)


if __name__ == '__main__':
    M = 50
    angles = [45, 0]
    l1, l2 = 5., 2.
    m1, m2 = 1.0, 0.1

    masses, lengths = [m1, m2], [l1, l2]
    t, u = solve_ode(f, fu, M, t0, T, masses, lengths, angles, alpha=(1 + 1j)/2)
    get_the_gif(t, u, M)

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# パラメータ
c_1 = 1/9
c_2 = 1
L = 1/7
G = 0.1
R = 1/G
m_0 = -0.5
m_1 = -0.8
B_p = 1


def g(x):
    return m_0*x + (m_1 - m_0)*abs(x + B_p)/2 + (m_0 - m_1)*abs(x - B_p)/2


def equ(Y):
    f_1 = (G*(Y[1] - Y[0]) - g(Y[0])) / c_1
    f_2 = (G*(Y[0] - Y[1]) + Y[2]) / c_2
    f_3 = -Y[1] / L
    return np.array([f_1, f_2, f_3])


def runge_kutta(Y, h):
    k_1 = h * equ(Y)
    k_2 = h * equ(Y + k_1/2)
    k_3 = h * equ(Y + k_2/2)
    k_4 = h * equ(Y + k_3)
    return Y + (k_1 + 2*k_2 + 2*k_3 + k_4)/6


def main():
    G_list = [0.6, 0.61, 0.635, 0.65, 0.6525, 0.657, 0.7, 0.8]
    for j in G_list:
        G = j
        Y = np.array([0.01, 0.01, 0.01])
        h = 0.01
        ans = [[], [], []]
        for i in range(10000):
            Y = runge_kutta(Y, h)
            if i > 1000:
                for i in range(3):
                    ans[i].append(Y[i])
        print('G = {}'.format(G))
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(np.array(ans[0]), np.array(ans[1]), np.array(ans[2]))
        ax.set_xlabel("v_c1")
        ax.set_ylabel("v_c2")
        ax.set_zlabel("i_L")
        fig.savefig(f"img_{j}.png")


if __name__ == "__main__":
    main()

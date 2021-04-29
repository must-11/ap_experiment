import matplotlib.pyplot as plt
import numpy as np


def equation(Y, fric=0.1):
    f1 = Y[1]
    if Y[1] > 0:
        f2 = - Y[0] + F(Y[0], Y[1]) - fric
    elif Y[1] < 0:
        f2 = - Y[0] + F(Y[0], Y[1]) + fric
    else:
        f2 = - Y[0] + F(Y[0], Y[1])
    return np.array([f1, f2])


def F(x, v, f=5, L=4, eps=0.5):
    if v > 0:
        if (x > L - eps) & (x <= L):
            return (f * x / eps + f - L * f / eps)
        elif (x > L) & (x < L + eps):
            return (- f * x / eps + f + L * f / eps)
        else:
            return 0
    else:
        if (x > - L - eps) & (x <= - L):
            return - (f * x / eps + f + L * f / eps)
        elif (x > L) & (x < - L + eps):
            return - (- f * x / eps + f - L * f / eps)
        else:
            return 0


def runge_kutta(Y, h):
    k_1 = h * equation(Y)
    k_2 = h * equation(Y + k_1/2)
    k_3 = h * equation(Y + k_2/2)
    k_4 = h * equation(Y + k_3)
    return Y + (k_1 + 2*k_2 + 2*k_3 + k_4)/6


def main():
    Y = np.array([5, 0])
    h = 0.001

    ans = [[], []]
    t = []
    for i in range(50000):
        Y = runge_kutta(Y, h)
        t.append(h * (i + 1))
        for j in range(2):
            ans[j].append(Y[j])

    print('初期条件 (x, v) = (5, 0)')
    plt.plot(ans[0], ans[1])
    plt.xlabel('x(t)')
    plt.ylabel('v(t)')
    fig.savefig("img01.png")

    plt.plot(t, ans[0])
    plt.xlabel('t')
    plt.ylabel('x(t)')
    fig.savefig("img02.png")

    plt.plot(t, ans[1])
    plt.xlabel('t')
    plt.ylabel('v(t)')
    fig.savefig("img03.png")


if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import numpy as np

# パラメータ
g = 9.8
l_1 = 0.5
l_2 = 0.5
m_1 = 0.5
m_2 = 0.3
w = np.sqrt(g / l_1)
l = l_2 / l_1
M = m_2 / (m_1 + m_2)
h = 0.01
t = 100
n = np.int(t / h)


def f(Y):
    d = Y[0] - Y[1]
    d1 = np.square(Y[2])
    d2 = np.square(Y[3])
    w2 = np.square(w)

    f_1 = (w2*l*(-np.sin(Y[0]) + M * np.cos(d) * np.sin(Y[1])) - M*l*(d1 * np.cos(d) + l * d2)*np.sin(d)) / (l - M*l*np.square(np.cos(d)))
    f_2 = (w2*np.cos(d)*np.sin(Y[0]) - w2*np.sin(Y[1]) + (d1 + M*l*d2*np.cos(d))*np.sin(d)) / (l - M*l*np.square(np.cos(d)))
    return np.array([Y[2], Y[3], f_1, f_2])


def exp_euler(Y, h):
    return Y + h * f(Y)


def H(Y):
    d = Y[0] - Y[1]
    d1 = np.square(Y[2])
    d2 = np.square(Y[3])

    T = m_1*np.square(l_1)*d1/2 + (np.square(l_1)*d1 + np.square(l_2)*d2 + 2*l_1*l_2*Y[2]*Y[3]*np.cos(d))*m_2/2
    U = -m_1*l_1*g*np.cos(Y[0]) - m_2*g*(l_1*np.cos(Y[0]) + l_2*np.cos(Y[1]))
    return T + U


def main():
    Y = np.array([0.1, 0, 0, 0])
    theta = [[0.1], [0]]
    ham = [H(Y)]
    for i in range(n):
        Y = exp_euler(Y, h)
        theta[0].append(Y[0])
        theta[1].append(Y[1])
        ham.append(H(Y))

    x = [i*0.01 for i in range(len(theta[0]))]
    fig = plt.figure(figsize=(12, 8))
    plt.plot(x, theta[0], label="theta1")
    plt.plot(x, theta[1], label="theta2")
    plt.xlabel('time', fontsize=14)
    plt.legend(loc='upper right')
    fig.savefig("img01.png")

    fig = plt.figure(figsize=(12, 8))
    plt.plot(x, ham, label="Hamiltonian")
    plt.xlabel('time', fontsize=14)
    plt.legend(loc='upper right')
    fig.savefig("img02.png")


if __name__ == "__main__":
    main()

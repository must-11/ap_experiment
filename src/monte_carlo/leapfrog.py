import matplotlib.pyplot as plt


class Hamiltonian:
    def __init__(self, sigma):
        self.sigma = sigma  # 2x2
        self.det = 1 / (self.sigma[0][0] * self.sigma[1][1] - self.sigma[0][1] * self.sigma[1][0])

    def get_value(self, q, p):
        value = ((self.sigma[0][0] * q[0]**2 - (self.sigma[0][1] + self.sigma[1][0]) * q[0] * q[1] + self.sigma[1][1] * q[1]**2) * self.det \
                        + p[0]**2 + p[1]**2) / 2
        return value

    def dq(self, q, idx=0):
        if idx==0:
            return (2 * self.sigma[0][0] * q[0] - (self.sigma[0][1] + self.sigma[1][0]) * q[1]) * self.det / 2
        elif idx==1:
            return (2 * self.sigma[1][1] * q[1] - (self.sigma[0][1] + self.sigma[1][0]) * q[0]) * self.det / 2


def step(q, p, H, h):
    p_ = p.copy()
    q_ = q.copy()
    for i in range(2):
        p_[i] -= (h / 2) * H.dq(q_, idx=i)
        q_[i] += h * p_[i]
        p_[i] -= (h / 2) * H.dq(q_, idx=i)

    return q_, p_, H.get_value(q_, p_)


def leapfrog(q, p, sigma, h, L):
    q_history = [[q[0]], [q[1]]]
    p_history = [[p[0]], [p[1]]]
    H = Hamiltonian(sigma)
    H_history = [H.get_value(q, p)]

    for _ in range(L):
        q, p, H_ = step(q, p, H, h)
        for i in range(2):
            q_history[i].append(q[i])
            p_history[i].append(p[i])
        H_history.append(H_)
    return q_history, p_history, H_history


def main():
    sigma = [[1, 0.95], [0.95, 1]]
    q = [-1.5, -1.55]
    p = [-1, 1]
    h = 0.25
    L = 30

    q_history, p_history, H_history = leapfrog(q, p, sigma, h, L)

    fig = plt.figure(figsize=(12, 5))
    plt.subplot(1,2,1)
    plt.plot(q_history[0], q_history[1], linewidth = 1.)
    plt.xlabel('q_1', fontsize = 14)
    plt.ylabel('q_2', fontsize = 14)
    plt.title('a locus of q')

    plt.subplot(1,2,2)
    plt.plot(p_history[0], p_history[1], linewidth = 1.)
    plt.xlabel('p_1', fontsize = 14)
    plt.ylabel('p_2', fontsize = 14)
    plt.title('a locus of p')
    fig.savefig("img01.png")

    fig = plt.figure(figsize=(12, 5))
    plt.plot([i for i in range(len(H_history))], H_history, linewidth = 1.)
    plt.xlabel('step', fontsize = 14)
    plt.ylabel('H', fontsize = 14)
    plt.title('a locus of H')
    fig.savefig("img02.png")

if __name__ == "__main__":
    main()

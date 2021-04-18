from collections import deque

import numpy as np


def make_Gm(G, match):
    n = G.shape[0]
    Gm = np.zeros((2*n, 2*n), dtype=np.int8)

    Gm[: n, n: ] = G.copy()
    for i, j in enumerate(match):
        if j != -999:
            Gm[j, i] = 1
    return Gm


def trans_match(match):
    n = len(match)
    match_ = np.array([-999]*n)
    for i, j in enumerate(match):
        if j != -999:
            match_[j - n] = i
    return match_


def dfs(u, G, color, n, parents):
    color[u] = 1
    if u >= n:
        for v in range(n):
            if (G[u, v]==1) & (color[v]==0):
                parents[v] = u
                dfs(v, G, color, n, parents)
    else:
        for v in range(n, 2*n):
            if (G[u, v]==1) & (color[v]==0):
                parents[v] = u
                dfs(v, G, color, n, parents)

    color[u] = 2


def dfs_time(u, G, color, n, f, time):
    color[u] = 1
    if u >= n:
        for v in range(n):
            if (G[u, v]==1) & (color[v]==0):
                dfs_time(v, G, color, n, f, time)
    else:
        for v in range(n, 2*n):
            if (G[u, v]==1) & (color[v]==0):
                dfs_time(v, G, color, n, f, time)

    color[u] = 2
    f[u] = time.pop()
    time.append(f[u]+1)


def dfs_group(u, G, color, group, n):
    color[u] = 1
    if u >= n:
        for v in range(n):
            if (G[u, v]==1) & (color[v]==0):
                dfs_group(v, G, color, group, n)
    else:
        for v in range(n, 2*n):
            if (G[u, v]==1) & (color[v]==0):
                dfs_group(v, G, color, group, n)

    color[u] = 2
    group.append(u)


def max_matching(G):
    n = G.shape[0]
    match = np.array([-999]*n)
    Gm = make_Gm(G, match)
    for u in range(n):
        if match[u] == -999:
            color = [0]*(2*n)
            parents = [-1]*(2*n)
            dfs(u, Gm, color, n, parents)
            e = -1
            for i, v in enumerate(parents[n: ]):
                if (v != -1) & ((i+n) not in match):
                    e = i + n
                    break
            if e != -1:
                for _ in range(n):
                    s = parents[e]
                    match[s] = e
                    if s == u:
                        break
                    e = parents[s]
                Gm = make_Gm(G, match)
    return match


def remove(Gm, match):
    n = len(match)
    U_0 = np.where(match == -999)[0]
    V_8 = np.where(trans_match(match) == -999)[0] + n

    Gm_ = Gm.copy()
    Gm_[U_0] = 0
    Gm_[:, V_8] = 0
    return Gm_


def scc(Gm_, n):
    color = [0]*(2*n)
    f = np.array([-1]*(2*n))
    time = deque()
    time = ([0])
    for u in range(2*n):
        if color[u] == 0:
            dfs_time(u, Gm_, color, n, f, time)

    order = np.argsort(f)[::-1]
    color = [0]*(2*n)
    group = []
    out = []
    for i in order:
        if i not in out:
            g = []
            dfs_group(i, Gm_.T, color, g, n)
            group.append(g)
            out.extend(g)

    rank = []
    for g in group:
        rank.append(f[g].max())
    rank = np.argsort(rank)[::-1]
    return rank, group

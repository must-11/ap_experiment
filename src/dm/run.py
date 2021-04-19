import matplotlib.pyplot as plt
import numpy as np

np.random.seed(100)
p = 0.98    # スパース度
n = 100    # 行列のサイズ
l = [0]*int(p*100) + [1]*int((1-p)*100)

def main():
    # 対象のグラフ
    G = np.random.choice(l, n**2).reshape((n, -1)).astype(np.int8)
    # 最大マッチングを求める
    match = max_matching(G)
    # 残余グラフから不要な枝を取り除く
    Gm = make_Gm(G, match)
    Gm_ = remove(Gm, match)
    # 強連結成分分解とトポロジカルソート
    rank, group = scc(Gm_, n)
    # 行と列の並びを決める
    row = []
    col = []
    for i in rank:
        if len(group[i]) > 1:
            for j in group[i]:
                if j < n:
                    row.append(j)
                else:
                    col.append(j - n)

    U_0 = np.where(match == -999)[0]
    V_8 = np.where(trans_match(match) == -999)[0]
    row = list(U_0) + row
    col += list(V_8)

    for i in row:
        if G[i].max() == 0:
            row.remove(i)
            row.append(i)

    col_ = []
    for i in col:
        if G[:, i].max() == 0:
            col.remove(i)
            col_.append(i)
    col = col_ + col

    # 行列を並び替える
    G_ = G[row]
    G_ = G_[:, col]

    plt.subplots(figsize=(5, 5))
    plt.imshow((1-G_), cmap="gray")
    fig.savefig("img.png")

if __name__ == "__main__":
    main()

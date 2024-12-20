import numpy as np

def create_transition_matrix(p, rank_original=5, win_for_rankup=4):
    # 状態空間の設定
    states = []
    state_index = {}
    index = 0

    # 各階級の状態を生成
    for rank in range(rank_original, 0, -1):  # 階級: 5級から1級まで
        if rank == rank_original:
            points = range(0, win_for_rankup)
        else:
            points = range(-2, win_for_rankup)
        for point in points:
            states.append((rank, point))
            state_index[(rank, point)] = index
            index += 1
    states.append((0, 0))  # 吸収状態 (0級)
    state_index[(0, 0)] = index

    n = len(states)
    P = np.zeros((n, n))

    # 各状態に対して遷移を設定
    for (rank, point) in states:
        i = state_index[(rank, point)]

        if rank == 0:  # 吸収状態
            P[i, i] = 1
            continue

        # 勝利時の遷移
        if point >= 0:
            if point + 1 == win_for_rankup:
                next_state = (rank - 1, 0)
            else:
                next_state = (rank, point + 1)
        else:
            next_state = (rank, 1)
        P[i, state_index[next_state]] = p

        # 敗北時の遷移
        if rank == rank_original and point == 0:
            next_state = (rank, 0)
        else:
            if point - 1 == -3:
                next_state = (np.amin([rank + 1,rank_original]), 0)
            else:
                next_state = (rank, point - 1)
        P[i, state_index[next_state]] = 1 - p

    return P, state_index

def expected_matches_to_absorption(p, rank_original=5, win_for_rankup=4):
    P, state_index = create_transition_matrix(p,rank_original,win_for_rankup)

    absorbing_states = [state_index[(0, 0)]]  # 吸収状態
    transient_states = [i for i in range(P.shape[0]) if i not in absorbing_states]

    Q = P[np.ix_(transient_states, transient_states)]


    I = np.eye(Q.shape[0])
    N = np.linalg.inv(I - Q)

    t = np.sum(N, axis=1)
    return t[transient_states.index(state_index[(rank_original, 0)])]  # 初期状態 (5級ポイント0) からの試合数

# 勝率 p を指定
res_list = []
p_list = [0.30+0.05*i for i in range((100-30)//5+1)]
for p in p_list:
    res_list.append(expected_matches_to_absorption(p,5,4))
print(res_list)

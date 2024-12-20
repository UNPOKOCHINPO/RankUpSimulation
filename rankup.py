import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
plt.rcParams["font.family"] = "MS Gothic"

def simulate_matches(p, num_simulations=10001, rank = 5, win_for_rankup = 4, lose_for_rankdown = 3):
    """
    シミュレーションを実行して、0級に昇格するまでの平均対戦数を計算する。

    Args:
        p (float): 勝率 (0 <= p <= 1)
        num_simulations (int): シミュレーション回数
        rank: 次の段までの階級の数
            ダイヤ帯ならマスター帯到達まで5回昇格する必要があるので、rank=5
            マスター帯ならマスター1到達まで4回昇格する必要があるので、rank=4
        win_for_rankup: 1つ階級を昇格するのに必要な勝ち点
        lose_for_rankdown: 勝ち点0の時点から、この数だけ連敗すると降格

    Returns:
        float: 対戦数の中央値 or 平均値
    """
    assert(num_simulations%2==1)

    total_matches = 0
    rank_original = rank
    match_list = []

    for _ in range(num_simulations):
        rank = rank_original
        points = 0
        matches = 0

        while rank > 0:
            matches += 1

            if random.random() < p:
                if points < 0:
                    points = 1  
                else:
                    points += 1

                if points == win_for_rankup:
                    rank -= 1
                    points = 0
            else:
                points -= 1

                if points == -lose_for_rankdown:
                    if rank != rank_original:
                        rank += 1
                    points = 0
            
            # 1か月で5000対戦まともにできる人はいないのでこれを上限にしておく
            # こうしないとプログラムの実行が終わらない場合が出てくる
            if matches > 5000: 
                break

        total_matches += matches
        match_list.append(matches)

    match_list = sorted(match_list)

    #return match_list[(num_simulations+1)//2], match_list
    return sum(match_list)/len(match_list), match_list

def simulate(rank=5, win_for_rankup=4, lose_for_rankdown=3):
    representative_list = []
    probability_list = [0.4+delta*0.01 for delta in range(100-40+1)]
    p_for_plot = 0.6
    for p in tqdm(probability_list):
        if abs(p-p_for_plot)<=1e-5:
            representative_matches, match_list = simulate_matches(p, rank=rank, win_for_rankup=win_for_rankup, lose_for_rankdown=lose_for_rankdown)
        else:
            representative_matches, _ = simulate_matches(p, rank=rank, win_for_rankup=win_for_rankup, lose_for_rankdown=lose_for_rankdown)
        representative_list.append(representative_matches)
    print([representative_list[i*5] for i in range(len(probability_list)//5 + 1)])

    if win_for_rankup == 4:
        plt.plot(probability_list, representative_list, marker='o', ms=3, label=('ダイヤ帯突破の平均対戦数'))
    else:
        plt.plot(probability_list, representative_list, marker='o', ms=3, label=('マスター1到達の平均対戦数'))
        plt.axhline(y=20, color='red', linestyle='--', linewidth=2, label='y=20')

    plt.xlabel("win probability")
    plt.ylabel("number of matches (representative)")
    plt.title("simulation result")
    plt.xlim(0.40,1.0)
    plt.ylim(0,800)
    
    plt.xticks(np.arange(0.40, 1.01, 0.05))  # x軸の目盛りを0.5ごと
    plt.yticks(np.arange(0, 801, 50))   # y軸の目盛りを50ごと

    # グリッドを有効化
    plt.grid(which='both', linewidth=0.3, color='gray')

    return match_list


def plot_hist(match_list, win_for_rankup):
    min_value = 0#np.amin(match_list)
    max_value = 400#np.amax(match_list)

    # ビンの範囲を20刻みで設定
    bins = np.arange(min_value, max_value + 10, 10)

    # ヒストグラムをプロット
    plt.hist(match_list, bins=bins, edgecolor='black')
    plt.xlabel('Value Range')
    plt.ylabel('Frequency')
    if win_for_rankup == 4:
        plt.title(f'ダイヤ帯突破までの対戦回数分布(p={p_for_plot})')
    else:
        plt.title(f'マスター1到達までの対戦回数分布(p={p_for_plot})')
    plt.savefig(f"hist{win_for_rankup}.png")
    plt.close("all")



if __name__ == "__main__":
    
    match_list45 = simulate(win_for_rankup=4, rank=5) # ダイヤ5 → マスター5
    match_list54 = simulate(win_for_rankup=5, rank=4) # マスター5 → マスター1

    plt.legend()
    plt.savefig("result.png")
    plt.close("all")


    # 最小値と最大値を取得
    p_for_plot = 0.6

    plot_hist(match_list45, win_for_rankup=4)
    plot_hist(match_list54, win_for_rankup=5)
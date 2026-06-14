from blackjack.simulation import simulate


def running_total(results):
    psa = [0] * len(results)
    psa[0] = results[0]
    for i in range(1, len(psa)):
        psa[i] = results[i] + psa[i - 1]
    return psa


def process_results(results, NUM_HANDS):
    # Let's display most profit, least profit, and EV by storing our results in a prefix sum array.
    psa = running_total(results)
    print(f"Player EV per hand: {psa[-1]/NUM_HANDS*100:.2f}%")
    print(f"Largest profit (Bets): {max(psa)}")
    print(f"Largest loss (Bets): {min(psa)}")

    filename = "results.txt"
    with open(filename, 'w') as f:
        for i in range(len(results)):
            f.write(f"Running Total: {psa[i]}\t\t\t")
            if(results[i]==0):
                f.write("Tie.\n")
            elif(results[i]>0):
                f.write(f"Won {results[i]} betting units.\n")
            else:
                f.write(f"Lost {-results[i]} betting units.\n")


def run_bankroll_experiment(lengths, reps):
    data = {}
    for length in lengths:
        curves = []
        for _ in range(reps):
            results = simulate(length)
            curves.append(running_total(results))
        data[length] = curves
    return data


def plot_bankrolls(data, save_path="bankrolls.png", show=True):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lengths = sorted(data.keys())
    num_lengths = len(lengths)

    fig, axes = plt.subplots(num_lengths, 1, figsize=(10, 4 * num_lengths), squeeze=False)
    axes = axes.flatten()

    for ax, length in zip(axes, lengths):
        curves = data[length]
        hands = list(range(1, length + 1))

        for curve in curves:
            ax.plot(hands, curve, color="steelblue", alpha=0.15, linewidth=0.8)

        mean_curve = [sum(curve[i] for curve in curves) / len(curves) for i in range(length)]
        min_curve = [min(curve[i] for curve in curves) for i in range(length)]
        max_curve = [max(curve[i] for curve in curves) for i in range(length)]

        ax.fill_between(hands, min_curve, max_curve, color="steelblue", alpha=0.2, label="Min/Max band")
        ax.plot(hands, mean_curve, color="darkblue", linewidth=2, label="Mean")
        ax.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)

        mean_ev = mean_curve[-1] / length * 100
        ax.set_title(f"{length:,} hands — mean EV: {mean_ev:.2f}%")
        ax.set_xlabel("Hand number")
        ax.set_ylabel("Cumulative profit (bets)")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)

    fig.suptitle("Bankroll curves across simulation lengths", fontsize=14, y=1.01)
    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight", dpi=150)

    if show:
        plt.show()

    plt.close(fig)

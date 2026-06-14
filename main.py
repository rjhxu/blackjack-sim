from blackjack import run_bankroll_experiment, plot_bankrolls

def main():
    LENGTHS = [5_000, 10_000, 100_000]  # << different sim lengths
    REPS = 20                            # << trials per length

    data = run_bankroll_experiment(LENGTHS, REPS)
    plot_bankrolls(data, save_path="bankrolls.png", show=True)

if __name__ == "__main__":
    main()

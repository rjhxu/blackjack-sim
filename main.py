from blackjack import simulate, save_results


def main():
    NUM_HANDS = 1_000_000
    bet_size = 2
    result = simulate(NUM_HANDS, bet_size)

    save_results(result, "results.txt")
    

if __name__ == "__main__":
    main()
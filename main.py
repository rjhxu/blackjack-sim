from blackjack import simulate, process_results

def main():
    NUM_HANDS = 10_000_000 # << modify this value
    result = simulate(NUM_HANDS)
    process_results(result, NUM_HANDS)
if __name__ == "__main__":
    main()
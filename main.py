from blackjack import simulate, process_results

# This program allows users to test 

def main():
    NUM_HANDS = 1000
    result = simulate(NUM_HANDS)
    process_results(result, NUM_HANDS)
if __name__ == "__main__":
    main()
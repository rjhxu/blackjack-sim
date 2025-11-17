from blackjack import simulate, save_results

# This program allows users to test 

def main():
    NUM_HANDS = 100_000
    result = simulate(NUM_HANDS)
    # save_results(result, "results.txt")
    

if __name__ == "__main__":
    main()
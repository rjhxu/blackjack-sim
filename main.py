from blackjack import simulate, save_results, calculateEV

# This program allows users to test 

def main():
    NUM_HANDS = 1000
    result = simulate(NUM_HANDS)
    calculateEV(result, NUM_HANDS)
    # save_results(result, "results.txt")    
if __name__ == "__main__":
    main()
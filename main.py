from blackjack import simulate, process_results
from display import display

# This program allows users to test 

def main():
    NUM_HANDS = 1000000
    result = simulate(NUM_HANDS)
    process_results(result, NUM_HANDS)
    display(result)
if __name__ == "__main__":
    main()
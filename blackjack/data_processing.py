#TODO
# display data with matplotlib?
# provide player largest loss/win streaks

def calculateEV(results, NUM_HANDS):
    print(f"Player EV per hand: {sum(results)/NUM_HANDS*100:.2f}%")

def save_results(results, filename):
    print()
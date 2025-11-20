def process_results(results, NUM_HANDS):
    # Let's display most profit, least profit, and EV by storing our results in a prefix sum array.
    psa = [0]*len(results)
    psa[0] = results[0]
    for i in range(1, len(psa)):
        psa[i] = results[i]+psa[i-1]
    print(f"Player EV per hand: {psa[-1]/NUM_HANDS*100:.2f}%")
    print(f"Largest profit (Bets): {max(psa)}")
    print(f"Largest loss (Bets): {min(psa)}")
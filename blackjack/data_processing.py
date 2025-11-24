def process_results(results, NUM_HANDS):
    # Let's display most profit, least profit, and EV by storing our results in a prefix sum array.
    psa = [0]*len(results)
    psa[0] = results[0]
    for i in range(1, len(psa)):
        psa[i] = results[i]+psa[i-1]
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
    
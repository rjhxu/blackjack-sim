This program performs Monte Carlo simulations of blackjack games to analyze the expected value (EV) of playing according to basic strategy. The simulation uses casino-style rules and can run millions of hands to produce statistically significant results.

## Game Rules

- **S17**: Dealer stands on soft 17
- **Continuous shuffle**: Each card is drawn independently (infinite deck)
- **RSA**: Re-split aces allowed
- **DAS**: Double after split allowed
- **Infinite splitting**: No limit on number of splits
- **Hit aces after splitting**: Players can hit aces after splitting them
- **Blackjack pays 3:2**: Natural blackjacks pay 1.5× the bet

## Running the Program

Run `main.py`. It runs multiple repeated simulations across configurable sample lengths and produces a bankroll visualization.

Adjust `LENGTHS` (hands per trial) and `REPS` (trials per length) in `main.py` to trade off accuracy vs. runtime.

## Output

- **`bankrolls.png`**: Cumulative profit curves per simulation length, with individual trials, mean line, and min/max band
- **`process_results()`** (available separately): Prints EV, peak profit, and peak loss; writes per-hand detail to `results.txt`

## Modifying the Program

- **`strategy.py`**: Player strategy tables
- **`dealer.py`**: House rules and dealer behavior
- **`simulation.py`**: Payout logic and game flow
- **`data_processing.py`**: Result analysis and plotting

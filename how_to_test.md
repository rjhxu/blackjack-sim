Run all tests with pytest -v

Automated Testing:

We should pass all 47 tests.

All tests should pass. The test suite includes:

test_deal_card.py: Validates card dealing logic and ace conversion
test_strategy.py: Verifies basic strategy is correctly implemented
test_dealer.py: Tests dealer behavior and S17 rules
test_simulation.py: Validates game simulation and outcomes
test_player.py: Tests player behaviour

What the Automated Tests Cover

Card Dealing: Ensures cards are valid values and aces convert properly when busting
Basic Strategy: Verifies all hard, soft, and pair decisions match optimal strategy
Dealer Logic: Confirms dealer follows S17 rules and correctly identifies blackjack
Game Simulation: Tests that games produce valid outcomes with correct payouts

Manual Testing
While automated tests cover the core logic, some aspects require manual verification to ensure the user interface works as expected.

Manual Test 1: Program execution

Steps
1. Run main.py
2. Wait for completion (depends on the simulation size)

Expected result:
Program completes without errors.
All 3 lines of output are dispalyed.
results.txt is created/overwritten.

Manual Test 2: Statistical Accuracy

Steps:
1. Pick a sample size (the amount of variance you'll see is inversely related to the size of the simulation)
2. Verify that the result makes sense

Expected result:
Large variance with smaller sample size (-10% to 10% with sizes of less than 1000)
Fast completion with small sample size
Low variance at a large sample size (-0.5% to -0.75% with sizes greater than 1_000_000)
Long execution times a large sample size. Ranging from a few seconds at one million to over a minute at 10_000_000
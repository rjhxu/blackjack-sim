Overview
This document explains the comprehensive testing strategy for the Blackjack Monte Carlo Simulation. 
The test suite covers all testable functions, plus manual tests for user interface verification.

Automated Test Coverage

test_deal_card.py coverage:

test_draw_card_frequency: Statistical test that verifies draw_card() produces the correct frequency of 10-value cards. Draws 1 million cards and confirms that approximately 4/13 (30.77%) are 10s (representing 10, J, Q, K). Uses pytest.approx with 1% tolerance to account for statistical variance.
test_draw_card_returns_valid_value: Validates that draw_card() only returns valid blackjack card values (2-11) over 1,000 draws. Ensures no invalid values ever appear.
test_add_card_no_aces: Tests adding cards when no aces are present in the hand. Verifies that the ace count can only be 0 (if non-ace drawn) or 1 (if ace drawn), and total remains valid (12-21).
test_add_card_with_ace_no_bust: Tests adding a card to a hand containing one ace (soft 11). Confirms the minimum resulting total is 12 (soft ace + 2), covering the ace-handling logic.
test_add_card_ace_converts_on_bust: Critical test for ace conversion. Starts with soft 20 (20 with one ace counted as 11), adds a card, and verifies that either the hand stays under 21 OR the ace has been converted (aces becomes 0).
test_add_card_multiple_aces: Tests the complex scenario of multiple aces. Starts with two aces (12 total, one soft), adds a card, and verifies proper handling. If the result is 12 or over 21, all soft aces should have been converted.

test_strategy.py coverage:

test_hard_strategy_always_hit_low_totals: Verifies hitting on hard 5-8 against all dealer upcards (2-11). Tests 4 totals × 10 upcards = 40 combinations.
test_hard_strategy_always_stand_17_plus: Confirms standing on hard 17-21 against all dealer upcards. Tests 5 totals × 10 upcards = 50 combinations. Critical rule verification.
test_hard_strategy_double_11_vs_2_through_10: Tests optimal doubling on hard 11 vs dealer 2-10 (9 combinations).
test_hard_strategy_hit_11_vs_ace: Verifies the exception where player hits (not doubles) 11 vs dealer Ace.
test_hard_strategy_double_10_vs_2_through_9: Tests doubling hard 10 vs dealer 2-9 (8 combinations).
test_hard_strategy_hit_10_vs_10_or_ace: Tests exceptions where player hits 10 vs dealer 10 or Ace (2 combinations).
test_hard_strategy_stand_13_16_vs_2_6: Verifies standing on stiff hands (13-16) vs dealer bust cards (2-6). Tests 4 totals × 5 upcards = 20 combinations.
test_hard_strategy_hit_13_16_vs_7_plus: Tests hitting stiff hands vs strong dealer cards (7-Ace). Tests 4 totals × 5 upcards = 20 combinations.
test_soft_strategy_always_stand_19_21: Confirms standing on strong soft hands (19-21) against all dealer upcards. Tests 3 totals × 10 upcards = 30 combinations.
test_soft_strategy_double_a6_vs_3_6: Tests doubling soft 17 (A-6) vs dealer 3-6 (4 combinations).
test_soft_strategy_hit_a6_vs_2_7_plus: Verifies hitting soft 17 vs dealer 2 and 7-Ace (5 combinations).
test_soft_strategy_a7_complex: Comprehensive test for A-7 (soft 18) with its complex strategy.
test_soft_strategy_double_a4_a5_vs_4_6: Tests doubling A-4 and A-5 (soft 15-16) vs dealer 4-6. Tests 2 totals × 3 upcards = 6 combinations.
test_pair_strategy_always_split_aces: Verifies always splitting Aces against all dealer upcards (10 combinations). Critical pair strategy rule.
test_pair_strategy_always_split_eights: Confirms always splitting 8s against all dealer upcards (10 combinations). Critical pair strategy rule.
test_pair_strategy_never_split_tens: Tests that player never splits 10s against any dealer upcard (10 combinations). Critical rule for optimal play.
test_pair_strategy_fives_treated_as_ten: Verifies that 5-5 is treated as hard 10 (double vs 2-9, hit vs 10-A). Tests 10 combinations.
test_pair_strategy_nines_stand_vs_7_10_ace: Tests that 9-9 stands vs dealer 7, 10, Ace (3 combinations).
test_pair_strategy_nines_split_vs_2_6_8_9: Verifies 9-9 splits vs dealer 2-6 and 8-9 (7 combinations).
test_pair_strategy_returns_valid_decision: Comprehensive validation test ensuring all pair strategies return valid decision codes (0-3) for all possible combinations. Tests 10 pair values × 10 upcards = 100 combinations.

test_dealer.py coverage:

test_dealer_returns_two_values: Validates that the dealer function returns a tuple of exactly 2 elements (total, upcard).
test_dealer_upcard_valid: Runs 100 dealer hands and ensures every upcard is a valid card value (2-11). Validates first card dealing.
test_dealer_final_total_valid: Verifies over 100 hands that dealer always ends with valid totals: 17-21 (valid hand), -1 (bust), or -2 (blackjack). No intermediate or invalid totals.
test_dealer_blackjack_detection: Probabilistic test running 1,000 hands to find at least one dealer blackjack. When found, verifies the upcard is 10 or Ace (required for blackjack). Tests early blackjack detection logic.
test_dealer_stands_17_or_higher: Validates S17 rule compliance over 100 hands. Confirms that when dealer doesn't bust or get blackjack (total > 0), the total is always 17-21, proving dealer stands on all 17s.
test_dealer_no_invalid_totals: Comprehensive validation over 200 hands ensuring dealer never returns invalid totals. Positive totals must be ≥17 (standing total), negative totals must be exactly -1 (bust) or -2 (blackjack). This catches any logic errors in the dealer hitting loop.

test_player.py coverage:

test_player_results_format: Validates that player returns a list where each element has exactly 2 components [total, doubled]. Runs 50 hands to ensure consistent format.
test_player_totals_valid: Over 100 hands, verifies that all player totals are valid: -2 (natural blackjack), -1 (bust), or 4-21 (standing totals). Ensures no invalid intermediate totals appear in results.
test_player_can_win: Probabilistic test confirming player can achieve winning totals (17-21) when dealer shows 6 (favorable card). Runs up to 100 hands to find at least one winning total.
test_player_can_bust: Probabilistic test verifying player can bust when facing dealer 10 (strong card). Searches 100 hands for at least one bust (-1), confirming hitting logic works.
test_player_can_double: Tests that player doubles down in appropriate situations. With dealer showing 5 (very favorable), searches 200 hands for at least one doubled hand, confirming double-down logic executes.
test_player_multiple_hands_from_split: Verifies split functionality by checking for results with multiple hands. With dealer showing 6 (favorable for splitting), searches 500 hands for at least one multi-hand result, confirming split execution.
test_player_blackjack_detection: Probabilistic test over 1,000 hands to find at least one natural blackjack (-2). When found, verifies the hand is not marked as doubled (blackjacks can't be doubled). Tests the special blackjack detection logic.
test_player_21_vs_blackjack: Tests the distinction between natural 21 (blackjack) and 21 from splits/hits. Verifies that split aces hitting 21 are treated as regular 21, not blackjack. Implicit validation through other tests.
test_construct_hand_pair_detection: Tests the construct_hand() helper function's pair detection logic. Over 200 hands, verifies that both pairs and non-pairs occur, and that pairs have even totals (except with aces). Validates the pair boolean in hand structure.
test_construct_hand_ace_handling: Tests construct_hand() when starting card is an ace (11). Searches 100 hands for aces and verifies totals are valid (≥12 or exactly 2 if double ace). Confirms ace handling in hand construction.
test_player_all_hands_resolved: Validates that all player hands are fully resolved to final totals over 100 hands. Ensures no intermediate values (like 5-11 without proper standing/hitting decision) appear in results. Confirms the player decision loop completes properly for all hands.

test_simulation.py coverage:

test_play_game_blackjack_payout: Probabilistic test verifying blackjack payout of 1.5 occurs. Runs 1,000 games to find at least one natural blackjack, confirming the special 3:2 payout logic in play_game().
test_play_game_push_occurs: Tests that ties (result = 0) occur in the simulation. Runs 500 games to find at least one push, validating the comparison logic when player and dealer totals match.
test_play_game_loss_occurs: Sanity check that player can lose. Runs 100 games to find at least one loss (negative result), confirming loss calculation logic works.
test_play_game_win_occurs: Sanity check that player can win. Runs 100 games to find at least one win (positive result), confirming win calculation logic works.

test_data_processing.py coverage:

test_process_results_handles_all_wins: Tests output formatting with all winning hands [1,1,1,1,1]. Verifies all three output lines appear.
test_process_results_handles_all_losses: Tests output with all losing hands [-1,-1,-1,-1,-1]. Ensures program handles negative results correctly.
test_process_results_handles_mixed_results: Tests realistic scenario with mixed outcomes [1,-1,1.5,-2,0,2,-1]. Validates handling of wins, losses, pushes, blackjacks, and doubles together.
test_process_results_correct_ev_all_wins: Validates EV calculation accuracy with all wins [1,1,1,1,1]. Expected EV = 100%. Confirms calculation: (sum/num_hands) × 100.
test_process_results_correct_ev_all_losses: Validates EV calculation with all losses [-1,-1,-1,-1,-1]. Expected EV = -100%. Tests negative EV display.
test_process_results_correct_ev_break_even: Tests zero EV scenario with balanced wins/losses [1,-1,1,-1]. Verifies 0.00% display.
test_process_results_handles_blackjack_payout: Tests EV calculation with 1.5 payouts [1.5,1.5]. Expected EV = 150%. Validates floating-point result handling.
test_process_results_largest_profit: Tests maximum profit calculation using results [1,1,1,-1,-1]. Prefix sum: [1,2,3,2,1]. Maximum = 3. Validates prefix sum algorithm and max() function.
test_process_results_largest_loss: Tests maximum loss calculation using results [-1,-1,-1,1,1]. Prefix sum: [-1,-2,-3,-2,-1]. Minimum = -3. Validates min() function on prefix sum.
test_process_results_with_doubles: Tests doubled bet handling with results [2,-2,2,-2]. Net zero, EV = 0%. Confirms doubled bets (±2) are processed correctly.
test_process_results_handles_zero_results: Edge case test with all pushes [0,0,0,0,0]. Expected: EV=0%, profit=0, loss=0. Tests zero-value edge case.
test_process_results_single_hand: Edge case test with single result [1]. Verifies program handles minimum input size correctly.
test_process_results_output_format: Validates that output contains all required information lines and text formatting. Checks for "Player EV", "Largest profit", "Largest loss" strings in output.
test_process_results_correct_lines: Ensures exactly 3 lines of output are produced. Verifies output structure consistency.

Test Coverage Summary
Note on coverage: The player and simulation modules use probabilistic logic with many conditional branches for different game outcomes. While core logic is fully tested, some rare edge case combinations (like 4+ sequential splits or specific card sequences) are validated probabilistically rather than deterministically. All critical paths are covered.

What Cannot Be Tested Automatically
User Interface Elements

The following aspects require manual testing as they involve user interaction or output formatting:

Console Output Formatting: Visual appearance and readability of results
Program Runtime Performance: Execution time with various hand counts
Error Messages: Program behavior with invalid configurations
User Workflow: Overall experience of running the simulation

Manual Test Procedures
Manual Test 1: Output Readability
What to test: Visual formatting of results
How to test:

Run python main.py
Verify output has exactly 3 lines
Confirm EV shows percentage with 2 decimals
Verify profit/loss values are clearly labeled

Expected: Clean output format:
Player EV per hand: -0.48%
Largest profit (Bets): 127
Largest loss (Bets): -143

Manual Test 2: Statistical Convergence
What to test: Large samples stay within our expected EV range
How to test:

Run main.py with a large sample size (>=5_000_000)
Record EV results
Repeat
Verify that EV consistently in the -0.4% to -0.75% range

Expected: Consistent negative EV for the player

Limitations

Probabilistic Tests: Some tests rely on randomness and could theoretically fail by chance (probability < 0.1%)
Rare Combinations: Some extreme scenarios (e.g., 5+ splits in one hand) are not explicitly tested
Performance: No automated regression tests for execution speed

Recommended Additional Testing
For production systems, consider:

Property-based testing with Hypothesis library
Longer statistical validation runs (100M+ hands)
Performance benchmarking suite
Memory usage profiling
Stress tests with extreme parameters (1B+ hands)


Conclusion
The test suite provides comprehensive coverage of all program functionality. The automated tests run in under 10 seconds and provide immediate feedback during development. 
Combined with manual testing procedures, this strategy ensures the simulation produces valid results that match theoretical expectations for blackjack with basic strategy.
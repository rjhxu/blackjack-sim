# Test Coverage

Overview of the testing strategy for the Blackjack Monte Carlo Simulation. The suite contains **87 tests** across six files. With matplotlib installed, all run; without it, 85 pass and 2 plot tests skip.

## Test Files

### test_deal_card.py (6 tests)

- **test_draw_card_frequency**: 1M draws confirm ~4/13 of cards are 10-value
- **test_draw_card_returns_valid_value**: All draws return values in 2–11
- **test_add_card_no_aces**: Adding to a hard hand produces valid totals
- **test_add_card_with_ace_no_bust**: Soft hand minimum total is 12
- **test_add_card_ace_converts_on_bust**: Ace demotes from 11 to 1 on bust
- **test_add_card_multiple_aces**: Multiple aces handled correctly

### test_strategy.py (18 tests)

Deterministic verification of all basic strategy tables:

- Hard totals: hit low hands, stand 17+, double 9–11, stand/hit 12–16 by upcard
- Soft totals: stand 19–21, double A-4 through A-7, complex A-7 (soft 18) rules
- Pairs: always split aces/8s, never split 10s, 5-5 as hard 10, 9-9 stand/split rules
- **test_pair_strategy_returns_valid_decision**: All 100 pair/upcard combos return 0–3

### test_dealer.py (11 tests)

Probabilistic validation plus deterministic S17 tests (via patched card sequences):

- Return format, valid upcards, valid final totals, blackjack detection
- **test_dealer_natural_blackjack**: A + 10 → (-2, 11)
- **test_dealer_stands_on_hard_17**: 10 + 7 → stands at 17
- **test_dealer_stands_on_soft_17**: A + 6 → stands at 17 (S17 rule)
- **test_dealer_hits_until_17**: 10 + 5 + 4 → hits then stands at 19
- **test_dealer_busts**: 10 + 6 + 10 → bust

### test_player.py (20 tests)

Probabilistic smoke tests plus deterministic decision-path tests:

- Result format, valid totals, win/bust/double/split detection, blackjack detection
- **test_player_splits_aces_even_vs_strong_upcard**: A,A vs dealer 10 → split (regression for ace-pair bug)
- **test_player_split_ace_21_is_not_natural_blackjack**: Split 21 ≠ -2
- **test_player_splits_non_ace_pair_and_seeds_correct_value**: 8,8 split seeds from 8
- **test_player_doubles_hard_11**: 5+6 double → 21 doubled
- **test_player_busts_when_hitting_stiff_hand**: 10+6 hit → bust
- **test_player_natural_blackjack**: A+10 → -2
- **test_player_hard_stand** / **test_player_soft_stand**: Stand paths
- **test_construct_hand_double_ace_is_soft_12_pair**: A,A → soft 12, still a pair

### test_simulation.py (19 tests)

Probabilistic outcome checks plus deterministic payout tests (via patched dealer/player):

- Win, loss, push, blackjack payout occurrence
- Dealer BJ: player loses (-1) or pushes (0) if also BJ
- Player beats/loses to dealer (normal and doubled bets)
- Push, bust (normal and doubled), 3:2 blackjack payout
- Player bust loses even when dealer busts
- Multi-hand summation from splits
- **test_simulate_returns_one_result_per_hand** / **test_simulate_zero_hands**

### test_data_processing.py (11 tests)

- **running_total**: Basic, doubles, single element, all losses
- **process_results**: EV/profit/loss output, per-hand file writing, negative EV
- **run_bankroll_experiment**: Structure and curve correctness
- **plot_bankrolls**: Saves PNG (skipped if matplotlib not installed)

## Coverage Summary

| Module | Coverage |
|--------|----------|
| `deal_card.py` | Full — dealing, ace conversion, multi-ace |
| `strategy.py` | Full — all table entries verified deterministically |
| `dealer.py` | Full — S17, BJ, bust, hit/stand branches |
| `player.py` | Full — stand, hit, double, split, BJ, bust, ace pairs |
| `simulation.py` | Full — all payout branches, multi-hand, simulate |
| `data_processing.py` | Full — running totals, EV output, experiment, plotting |

Deterministic tests use `monkeypatch` to force exact card sequences, removing reliance on randomness for critical paths. Probabilistic tests remain as sanity checks for general behavior.

## Manual Testing

See [`how_to_test.md`](how_to_test.md) for manual verification of program execution and statistical convergence.

## Limitations

- No automated performance regression tests
- Extreme scenarios (5+ sequential splits) are not individually tested
- Plot tests require matplotlib as an optional dependency

## Conclusion

The suite runs in under a second and covers every module and decision branch in the simulation. Combined with manual convergence checks, it validates that the program produces results consistent with theoretical expectations for basic-strategy blackjack.

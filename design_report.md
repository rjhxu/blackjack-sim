Design Report - Blackjack Monte Carlo Simulation

1. Introduction
This program performs Monte Carlo simulations of blackjack games to determine the expected value (EV) of playing with optimal basic strategy. 
Monte Carlo simulations are a statistical technique that uses repeated random sampling to obtain numerical results. 
In this case, we simulate millions of blackjack hands to understand the probability distribution of outcomes and calculate the player's expected return.
The simulation models a realistic casino blackjack game with specific rules (as listed in instructions.md). 
The player follows mathematically optimal basic strategy, which has been proven to minimize the house edge.
The purpose of this project is to demonstrate Monte Carlo methods, to validate basic strategy effectiveness, and to understand the variance inherent in blackjack even with optimal play. 
The simulation outputs the expected value per hand, as well as the maximum profit and loss observed during the session.

2. Design
The program is designed with a modular architecture that separates concerns into distinct, testable components. 
This design philosophy ensures that each function has a single, well-defined responsibility, making the code easier to test, maintain, and extend.

The codebase is organized into a blackjack module containing six files, each responsible for a specific aspect of the simulation:
deal_card.py: Provides low-level card dealing functionality. The draw_card() function simulates drawing from an infinite deck (continuous shuffle) by randomly selecting from valid card values. The add_card() function handles the complex logic of adding a card to a hand while automatically converting aces from 11 to 1 when necessary to prevent busting.

strategy.py: Contains the basic strategy tables and lookup functions. Basic strategy is encoded as 2D arrays mapping player totals and dealer upcards to optimal decisions. Three separate functions handle hard totals, soft totals (hands with aces), and pairs, each returning a decision code (0=stand, 1=hit, 2=double, 3=split).

dealer.py: Implements dealer behavior in isolation. The dealer() function deals two cards to the dealer, checks for blackjack, and follows the S17 rule (stand on all 17s). It returns both the dealer's final total and upcard, using special codes (-2 for blackjack, -1 for bust).

player.py: Implements player decision-making and hand management. The player() function handles the complexity of multiple hands resulting from splits, maintaining a queue of hands to be played. It consults the strategy tables to make decisions and properly handles special cases like natural blackjacks on split aces.

simulation.py: Orchestrates the game flow and runs multiple simulations. The play_game() function combines dealer and player logic to simulate a complete hand, handling all possible outcomes and calculating the net result. The simulate() function runs multiple games and collects results.

data_processing.py: Processes and presents simulation results. The `running_total()` helper builds prefix-sum bankroll curves. `process_results()` calculates expected value and writes per-hand detail to a text file. `run_bankroll_experiment()` runs repeated simulations across multiple sample lengths. `plot_bankrolls()` visualizes cumulative profit curves with matplotlib — individual trials, mean line, and min/max band per length.

3. Design Highlights
Elegant Ace Handling
One of the first problems I ran into was handling aces, which can count as either 1 or 11. The solution implemented in add_card() handles it in the following format:
Rather than tracking whether a hand is "soft" or "hard," the code tracks the number of aces currently counted as 11. 
When the total exceeds 21, it automatically converts aces from 11 to 1 (subtracting 10) until either the hand is under 21 or all aces have been converted. 
This approach handles all edge cases, including multiple aces, without complex logic.

Tracking all hand information in integers
Looking to opimize for speed, I chose to store as much information in integer format to prevent costly string == string evaluations.
I also chose to store things like split in a queue which would allow us to quickly unpack information in simulation.py and compare with the strength of the dealer's hand.
When a pair is split, two new hands are added to the queue. The loop continues until all hands have been played. 
This approach handles arbitrary levels of splitting without recursion and maintains the correct order of play.

Other miscellaneous performance optimizations:
We used a prefix sum array when computing the EV adn the running total. This can also allow us to graphically display our results in the future.
The prefix sum array improves our performance drastically.
We used special values like -1 and -2 to encode results such as a bust or natural blackjack. evaluating these integers is marginally faster than evaluating string equality

4. Areas for improvement

Output
The program now includes matplotlib bankroll visualization (`plot_bankrolls`), but additional statistics would still provide more insight:

Standard deviation of results to measure volatility
Win/loss/push percentages
Distribution of outcomes (histogram)
Separate tracking of split, double, and regular hand results
Confidence intervals for the EV estimate

Static game rules
Right now dealer behaviour and game rules are hard coded into the program. A more robust simulation could feature simulations of an actual 2-8 deck shoe.
This would allow us to track both the running and true count and allow us to implement a player strategy that features counting. 
This could allow us to demonstrate a game with a positive player edge.
The basic strategy is hard-coded in strategy.py. While this is appropriate for demonstrating optimal play, it would be interesting to:

Support multiple strategy variations
Allow testing of non-optimal strategies
Implement strategy deviations based on true count (card counting)
Compare strategies side-by-side

This would require refactoring the strategy system to be more flexible, possibly using configuration files or strategy objects.

5. Lessons learned
Breaking the program into small, single-purpose functions made development significantly easier. 
When I encountered bugs (for example, initially treating player busts as pushes), I could isolate the problem to a specific function and fix it there. 
The modular design also made it straightforward to add features like split handling without rewriting existing code.

Writing pytest tests forced me to think through edge cases I had initially overlooked. 
For instance, I had to carefully consider what happens when the dealer shows an ace, when multiple aces are in a hand, and when hands are split multiple times. 

Keeping all I/O in separate functions from game logic made testing a lot easier. 
I could test game logic without worrying about capturing print output, and I could verify that the simulation logic works correctly independent of how results are displayed. 
This principle is applicable far beyond this project.

Early in development, I tested with small sample sizes (1,000-10,000 hands) and got wildly varying results. 
I learned that Monte Carlo simulations need sufficiently large sample sizes to converge on accurate estimates. 
With 10 million hands, the EV consistently converges to the expected -0.4% to -0.6% range, demonstrating that the simulation is working correctly.

I underestimated how long it would take to write clear, comprehensive documentation. 
Writing instructions, test plans, and this design report took nearly as long as writing the code itself.
However, the process of writing documentation revealed gaps in my understanding and helped me improve the code.

I followed the recommended iterative approach, starting with a minimal version (just dealing cards and comparing hands) and gradually adding features (splits, doubles, automated testing, documentation).
This approach meant I always had a working version to fall back on and could test each feature in isolation before adding the next one.
I really liked this approach because it made the project seem much easier by breaking it into smaller manageable tasks.
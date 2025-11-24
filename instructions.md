This program performs Monte Carlo simulations of blackjack games to analyze the expected value (EV) of playing according to basic strategy. 
The simulation uses simple casino rules and can play millions of hands to provide statistically significant results.

Game Rules:
The simulation uses the following blackjack rules:

S17: Dealer stands on soft 17
Continuous Shuffle: Each card is drawn independently (infinite deck simulation)
RSA: Re-split Aces allowed
DAS: Double After Split allowed
Infinite Splitting: No limit on number of splits
Hit Aces After Splitting: Players can hit aces after splitting them
Blackjack Pays 3:2: Natural blackjacks pay 1.5 times the bet

How to run the program:

Run the main.py file

Optional:
adjust the NUM_HANDS variable to simulate more or less hands for accuracy/performance

Output:
The program will display Expected Value, highest point of profit, and largest loss.

Modifying the program:
Both player and casino behaviour can also be modified to suit specific test cases
Users can modify strategy.py to adjust the players strategy, and modify dealer.py to adjust house rules
Furthermore, payouts and game quality can be adjusted in simulation.py
Lastly, users can use other librares in data_processing.py to adjust their programs
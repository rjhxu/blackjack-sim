# Basic Strategy for multi-deck S17 blackjack game. according to playsmart Ontario. https://www.playsmart.ca/wp-content/uploads/2019/03/PS.ca_BJ-Strat.pdf

hard = [
# A  2  3  4  5  6  7  8  9  10
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 6
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 7
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 8
 [1, 1, 2, 2, 2, 2, 1, 1, 1, 1],  # 9   -> double vs dealer 3-6
 [1, 2, 2, 2, 2, 2, 2, 2, 1, 1],  # 10  -> double vs dealer 2-9
 [1, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 11  -> double vs dealer 2-10 (hit vs A)
 [1, 1, 1, 0, 0, 0, 1, 1, 1, 1],  # 12  -> stand vs 4-6
 [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 13  -> stand vs 2-6
 [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 14
 [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 15
 [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 16
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17  -> always stand
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 20
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 21
]

soft = [
# A  2  3  4  5  6  7  8  9  10
 [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],  # A+2 (13) -> double vs 5-6
 [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],  # A+3 (14) -> double vs 5-6
 [1, 1, 1, 2, 2, 2, 1, 1, 1, 1],  # A+4 (15) -> double vs 4-6
 [1, 1, 1, 2, 2, 2, 1, 1, 1, 1],  # A+5 (16) -> double vs 4-6
 [1, 1, 2, 2, 2, 2, 1, 1, 1, 1],  # A+6 (17) -> double vs 3-6
 [1, 0, 2, 2, 2, 2, 0, 0, 1, 1],  # A+7 (18) -> stand except hit vs 9,10,A; double vs 3-6
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A+8 (19) -> always stand
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A+9 (20) -> always stand
]


pair = [
# A  2  3  4  5  6  7  8  9  10
 [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],  # A,A  -> always split
 [1, 3, 3, 3, 3, 3, 3, 1, 1, 1],  # 2,2  -> split vs 2-7 (DAS adds 2-3)
 [1, 3, 3, 3, 3, 3, 3, 1, 1, 1],  # 3,3  -> split vs 2-7 (DAS adds 2-3)
 [1, 1, 1, 1, 3, 3, 1, 1, 1, 1],  # 4,4  -> split only vs 5-6 (DAS required)
 [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],  # 5,5  -> treat as 10 (double vs 2-9)
 [1, 3, 3, 3, 3, 3, 1, 1, 1, 1],  # 6,6  -> split vs 2-6 (with DAS also vs 2)
 [1, 3, 3, 3, 3, 3, 3, 1, 1, 1],  # 7,7  -> split vs 2-7
 [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],  # 8,8  -> always split
 [0, 3, 3, 3, 3, 3, 0, 3, 3, 0],  # 9,9  -> split vs 2-6 and 8-9; stand vs 7,10,A
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10,10 -> never split (always stand)
]


def hard_strategy(total, upcard):
    '''Returns player decision according to strategy. 0 -> Stand. 1 -> Hit. 2 -> Double.'''
    return hard[total-5][upcard-2]
def soft_strategy(total, upcard):
    '''Returns player decision according to strategy. 0 -> Stand. 1 -> Hit. 2 -> Double.'''
    return hard[total-13][upcard-2]
def pair_strategy(pair, upcard):
    '''Returns player decision according to strategy. 0 -> Stand. 1 -> Hit. 2 -> Double. 3 -> Split'''
    return hard[pair-1][upcard-2]


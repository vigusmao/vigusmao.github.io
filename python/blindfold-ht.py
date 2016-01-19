from random import random


# ---------------------------------------------------------------------
#
# Please set the three constants below:

SIMULATION_LENGTH = 100000  # number of executions per value of p
START_PROB = 0.001          # the first value of p
INCREMENT = 0.001           # difference between subsequent values of p

# ---------------------------------------------------------------------


HEADS = 0
TAILS = 1
HANDCLAP = 0
WHISTLE = 1
BY_REFERENCE = 0


# ---------------------------------------------------------------------
#
#     toss coin
#
# ---------------------------------------------------------------------
def toss_coin(p, base):
    r = random()
    if r < p:
        face = HEADS
    else:
        face = TAILS

    if face == base[BY_REFERENCE]:
        sound = HANDCLAP # same as previous
    else:
        sound = WHISTLE  # different from previous
    
    base[BY_REFERENCE] = face
    return sound


# ---------------------------------------------------------------------
#
#     fair heads or tails with concealed biased coin
#
# ---------------------------------------------------------------------
def fair_heads_or_tails_with_concealed_biased_coin(p, total_tosses):

    base = [None]
    n_tosses = 0
    waiting_decision = False
        
    while True:
        sound = toss_coin(p, base)
        n_tosses += 1

        if n_tosses % 2 == 0:
            if sound == WHISTLE:
                waiting_decision = True
        else:
            if waiting_decision:
                total_tosses[BY_REFERENCE] += n_tosses
                if sound == WHISTLE:
                    return 1
                else:
                    return 2


# ---------------------------------------------------------------------
#
#     main
#
# ---------------------------------------------------------------------


print("\nNumber of executions for each coin bias: %d" % SIMULATION_LENGTH)
print("\np = probability of heads " +
      "\nw = average wins of Player 1 " +
      "\nt = average number of coin tosses" +
      "\n\np      w       t")


p = START_PROB
while p < 1:

    total_tosses = [0]
    n_victories_Player_1 = 0

    turns = 0
    while turns < SIMULATION_LENGTH:
        
        if fair_heads_or_tails_with_concealed_biased_coin(p, total_tosses) == 1:
            n_victories_Player_1 += 1

        turns += 1
        
    print("%.3f, %.4f, %.4f" % (p,
                                n_victories_Player_1 / SIMULATION_LENGTH,
                                total_tosses[BY_REFERENCE] / SIMULATION_LENGTH))

    p += INCREMENT
    

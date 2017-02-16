"""
Logic for the Risk Simulating Aspect of Game Helper

Developed by Zac Patel on 1/11/17
"""
# importing a function to handle random number generation
from random import randint

# importing methods for creating final, Alexa readable responses
from SpeechHelpers import build_speechlet_response, build_response

# --------------- Complete behavior functions that can be called by other files ---------------
def battle_handler(intent):
    intent = intent["slots"]
    # Taking advantage of python's ability to return multiple items
    # Reads the number of attackers and defenders from the intent
    num_attackers, num_defenders = get_num_att_def(intent)

    # simulates a battle to get the final number of attackers and defenders
    final_attackers, final_defenders, num_rounds = simulate_battle(num_attackers, num_defenders)

    # generates a battle summary string from the results
    battle_res_string = create_battle_res_string(num_attackers, num_defenders, final_attackers, final_defenders)

    # setting the title of the card that should appear on the phone app
    card_title = "Battle Simulated"

    session_attributes = {}
    # constructs and returns a completed Alexa response
    # note: no reprompt text is given because in the course of a game, a battle would only be run once
    return build_response(session_attributes, build_speechlet_response(card_title, battle_res_string, None, True))

def battle_probability_handler(intent):
    intent = intent["slots"]
    # read the number of attackers and defenders from the intent
    num_attackers, num_defenders = get_num_att_def(intent)

    # search the probability table for the corresponding probability
    prob = find_battle_probability(num_attackers, num_defenders)

    # construct a statement about the probability
    prob_res_str = create_prob_res_str(prob)

    # setting the title of the card that should appear on the phone app
    card_title = "Battle Probability Calculated"

    session_attributes = {}
    # construct a reply to the user
    return build_response(session_attributes, build_speechlet_response(card_title, prob_res_str, None, True))

# giving several possible phrases for variety (note, these are only given if the user asks for them)
pos_rec_phrases = ["I suggest you attack.", "The odds are in favor of attacking.", "You are likely to win."]
mid_rec_phrases = ["The fight could go either way.", "There is no obvious winner", "You could try your luck."]
neg_rec_phrases = ["I suggest you don't attack", "The odds are against attacking.", "You are not likely to win."]

def create_prob_res_str(prob, recommendation=False):
    """
    returns a string describing the probability of a battle the user created
    """
    prob_string = ""
    if prob == -1:
        prob_string = "This function can only predict battles between 10 or fewer units on each side. In general, attackers have advantage at higher army numbers."
    else:
        prob_string = "Attackers have a " + str(prob * 100) + " percent chance of winning the battle."

    # add a recommendation if the user wants one
    if recommendation:
        if prob > .6:
            prob_string = prob_string + pos_rec_phrases[randint(0, len(pos_rec_phrases)-1)]
        elif .4 <= prob <= .6:
            prob_string = prob_string + mid_rec_phrases[randint(0, len(mid_rec_phrases)-1)]
        else:
            prob_string = prob_string + neg_rec_phrases[randint(0, len(neg_rec_phrases)-1)]

    return prob_string
# ---------------Helper functions that should not be used outside of this file---------------
# (generally listed in the order in which they would be called)


def get_num_att_def(intent):
    """
    Reads the number of attackers and defenders from an intent, and returns them in an ordered pair"
    """
    # Determines in which order the user listed attackers and defenders
    num_party_one, num_party_two = int(intent["numPartyOne"]["value"]), int(intent["numPartyTwo"]["value"])
    party1Type, party2Type = int(intent["partyOneType"]["value"]), int(intent["partyTwoType"]["value"])

    # Attacker / Defender Keywords (to match custom type)
    attacker_keywords = {"attacker", "attacking", "attackers"}
    defender_keywords = {"defender", "defending", "defenders"}

    # default behavior for this statement is attackers first, then defenders second
    if party1Type in defender_keywords:
        return num_party_two, num_party_one
    else:
        return num_party_one, num_party_two

def simulate_battle(num_attackers, num_defenders):
    """
    simulates the entirety of a battle until the one side is defeated
    returns the number of remaining attackers, defenders and turns taken
    """
    # Tracker for the number of rounds needed to do the battle (just for funsies)
    num_rounds = 0

    # note, we include the attacker that is "left behind" in our calculations to better represent
    # how calculations would be done by hand
    # Each iteration of the while loop represents an individual "battle" / "dice roll"
    while num_attackers > 1 and num_defenders > 0:
        num_rounds += 1

        attacker_rolls, defender_rolls = [], []

        # including checks for the special cases where attackers / defenders have less than full strength
        if num_attackers > 3:
            attacker_rolls = generate_battle_rolls(3)
        else:
            attacker_rolls = generate_battle_rolls(num_attackers - 1)

        if num_defenders > 2:
            defender_rolls = generate_battle_rolls(2)
        else:
            defender_rolls = generate_battle_rolls(num_defenders)


        # sorting the rolls so we can compare the two highest rolls
        attacker_rolls.sort()
        defender_rolls.sort()

        # number of wins is measures from the attackers perspective
        # a "fight" in this instance is the comparison between two dice rolls
        wins, num_fights = 0, min(num_attackers -1, num_defenders)
        for i in range(0, num_fights):
            if attacker_rolls[i] > defender_rolls[i]:
                wins += 1

        # recalculating the number of attackers and defenders after the fight
        num_attackers, num_defenders = num_attackers - (num_fights - wins), num_defenders - wins

    return num_attackers, num_defenders, num_rounds

def generate_battle_rolls(numRolls):
    """
    Returns an array representing all the dice rolls by one side in a battle
    """
    return [randint(1, 6) for _ in range(0, numRolls)]

def create_battle_res_string(init_attackers, init_defenders, final_attackers, final_defenders):
    """
    reates a string summarizing the result of a battle
    """
    if final_defenders == 0:
        return "The attackers won a battle of " + str(init_attackers) + " vs " + str(init_defenders) + " with " + str(final_attackers) + " remaining."
    else:
        return "The defenders survived a battle of " + str(init_attackers) + " vs " + str(init_defenders) + " with " + str(final_defenders)+ "remaining."


def find_battle_probability(num_attackers, num_defenders):
    """
    Takes in a number of attackers and defenders (from 1-10)
    Returns the probability that the defenders will be defeated before attackers are forced to stop
    returns -1 if the number of armies is outside the bounds of the chart

    (may be adapted later to include full probability calculations)
    note this method adjusts for the attacker that must be left behind
    """
    if num_attackers > 12 or num_attackers <= 1 or  num_defenders > 11 or num_defenders < 1:
        return -1
    else:
        return prob_chart[num_attackers - 2][num_defenders - 1]

# Taken from Jason A. Osborne's paper: http://www4.stat.ncsu.edu/~jaosborn/research/RISK.pdf
# x -> attackers, y -> defenders
prob_chart = [
[0.417, 0.106, 0.027, 0.007, 0.002, 0.000, 0.000, 0.000, 0.000, 0.000],
[0.754, 0.363, 0.206, 0.091, 0.049, 0.021, 0.011, 0.005, 0.003, 0.001],
[0.916, 0.656, 0.470, 0.315, 0.206, 0.134, 0.084, 0.054, 0.033, 0.021],
[0.972, 0.785, 0.642, 0.477, 0.359, 0.253, 0.181, 0.123, 0.086, 0.057],
[0.990, 0.890, 0.769, 0.638, 0.506, 0.397, 0.297, 0.224, 0.162, 0.118],
[0.997, 0.934, 0.857, 0.745, 0.638, 0.521, 0.423, 0.329, 0.258, 0.193],
[0.999, 0.967, 0.910, 0.834, 0.736, 0.640, 0.536, 0.446, 0.357, 0.287],
[1.000, 0.980, 0.947, 0.888, 0.818, 0.730, 0.643, 0.547, 0.464, 0.380],
[1.000, 0.990, 0.967, 0.930, 0.873, 0.808, 0.726, 0.646, 0.558, 0.480],
[1.000, 0.994, 0.981, 0.954, 0.916, 0.861, 0.800, 0.724, 0.650, 0.568]
]
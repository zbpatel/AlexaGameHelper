"""
Logic for the Risk Simulating Aspect of Game Helper

Developed by Zac Patel on 1/11/17
"""
# importing a function to handle random number generation
from random import randint

# importing methods for creating final, Alexa readable responses
from SpeechHelpers import build_speechlet_response, build_response

# --------------- Complete behavior functions that can be called by other files ---------------
def RiskBattleHandler(intent):
    # Taking advantage of python's ability to return multiple items
    # Reads the number of attackers and defenders from the intent
    numAttackers, numDefenders = getNumAttDef(intent)

    # simulates a risk battle to get the final number of attackers and defenders
    finalAttackers, finalDefenders, numRounds = simulateRiskBattle(numAttackers, numDefenders)

    # generates a battle summary string from the results
    battleResultString = createRiskBattleResultString(numAttackers, numDefenders, finalAttackers, finalDefenders)

    # setting the title of the card that should appear on the phone app
    card_title = "Risk Battle Simulated"

    session_attributes = {}
    # constructs and returns a completed Alexa response
    # note: no reprompt text is given because in the course of a game, a battle would only be run once
    return build_response(session_attributes,
        build_speechlet_response(card_title, battleResultString, None, True))

def RiskProbabilityHandler(intent):
    # read the number of attackers and defenders from the intent
    numAttackers, numDefenders = getNumAttDef(intent)

    # search the probability table for the corresponding probability
    prob =  findRiskBattleProbability(numAttackers, numDefenders)

    # construct a statement about the probability
    probResponseString = createProbabilityResponseString(prob)

    # setting the title of the card that should appear on the phone app
    card_title = "Risk Probability Calculated"

    session_attributes = {}
    # construct a reply to the user
    return build_response(session_attributes,
        build_speechlet_response(card_title, probResponseString, None, True))

# giving several possible phrases for variety (note, these are only given if the user asks for them)
posRecPhrases = {"I suggest you attack.", "The odds are in favor of attacking.", "You are likely to win."}
midRecPhrases = {"The fight could go either way.", "There is no obvious winner", "You could try your luck."}
negRecPhrases = {"I suggest you don't attack", "The odds are against attacking.", "You are not likely to win."}

# creates a string describing the probability about a battle
def createProbabilityResponseString(prob, recommendation=False):
    probString = ""
    if prob == -1:
        probString = "This function can only predict battles between 10 or fewer units on each side. In general, attackers have advantage at higher army numbers."
    else:
        probString = "Attackers have a " + str(prob * 100) + " percent chance of winning the battle."

    # add a recommendation if the user wants one
    if recommendation:
        if prob > .6:
            probString = probString + posRecPhrases[randint(0, len(posRecPhrases))]
        elif .4 <= prob <= .6:
            probString = probString + midRecPhrases[randint(0, len(midRecPhrases))]
        else:
            probString = probString + negRecPhrases[randint(0, len(negRecPhrases))]

    return probString
# ---------------Helper functions that should not be used outside of this file---------------
# (generally listed in the order in which they would be called)

# Reads the number of attackers and defenders from an intent, and returns them in an ordered pair
def getNumAttDef(intent):
    # Determines in which order the user listed attackers and defenders
    numPartyOne, numPartyTwo = int(intent["numPartyOne"]["value"]), int(intent["numPartyTwo"]["value"])
    party1Type, party2Type = int(intent["partyOneType"]["value"]), int(intent["partyTwoType"]["value"])

    # Attacker / Defender Keywords (to match custom type)
    attackerKeywords = {"attacking", "attackers"}
    defenderKeywords = {"defender", "defending"}

    # default behavior for this statement is attackers first, then defenders second
    if (party1Type in defenderKeywords):
        return numPartyTwo, numPartyOne
    else:
        return numPartyOne, numPartyTwo

def simulateRiskBattle(numAttackers, numDefenders):
    # Tracker for the number of rounds needed to do the battle (just for funsies)
    numRounds = 0

    # note, we include the attacker that is "left behind" in our calculations to better represent
    # how calculations would be done by hand
    # Each iteration of the while loop represents an individual "battle" / "dice roll"
    while numAttackers > 1 and numDefenders > 0:
        numRounds += 1

        attackerRolls, defenderRolls = [], []

        # including checks for the special cases where attackers / defenders have less than full strength
        if numAttackers > 3:
            attackerRolls = generateRiskBattleRolls(3)
        else:
            attackerRolls = generateRiskBattleRolls(numAttackers - 1)

        if numDefenders > 2:
            defenderRolls = generateRiskBattleRolls(2)
        else:
            defenderRolls = generateRiskBattleRolls(numDefenders)


        # sorting the rolls so we can compare the two highest rolls
        attackerRolls.sort()
        defenderRolls.sort()

        # number of wins is measures from the attackers perspective
        # a "fight" in this instance is the comparison between two dice rolls
        wins, numFights = 0, min(numAttackers -1, numDefenders)
        for i in range(0, numFights):
            if attackerRolls[i] > defenderRolls[i]:
                wins += 1

        # recalculating the number of attackers and defenders after the fight
        numAttackers, numDefenders = numAttackers - (numFights - wins), numDefenders - wins

    return numAttackers, numDefenders, numRounds

# Returns an array representing all the dice rolls by one side in a battle
def generateRiskBattleRolls(numRolls):
    return [randint(1, 6) for _ in range(0, numRolls)]

# creates a string summarizing the result of a risk battle
def createRiskBattleResultString(initAttackers, initDefenders, finalAttackers, finalDefenders):
    if finalDefenders == 0:
        return "The attackers won a battle of " + str(initAttackers) + " vs " + str(initDefenders) + " with " + str(finalAttackers) + " remaining."
    else:
        return "The defenders survived a battle of " + str(initAttackers) + " vs " + str(initDefenders) + " with " + str(finalDefenders)+ "remaining."

# returns -1 if the number of armies is outside the bounds of the chart
# may be adapted later to include full probability calculations
# note this method adjusts for the attacker that must be left behind
def findRiskBattleProbability(numAttackers, numDefenders):
    if numAttackers > 12 or numAttackers <= 1 or  numDefenders > 11 or numDefenders < 0:
        return -1
    else:
        return riskProbabilityChart[numAttackers - 2][numDefenders - 1]

# Taken from Jason A. Osborne's paper: http://www4.stat.ncsu.edu/~jaosborn/research/RISK.pdf
# x -> attackers, y -> defenders
riskProbabilityChart = [
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
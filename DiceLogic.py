"""
Logic for the "Word Game" helper functions of the Game Helper Alexa Skill

Developed by Zac Patel on 2/15/17
"""
# importing random to allow for random number generation
from random import randint

# useful imports for building speech responses
from SpeechHelpers import build_response, build_speechlet_response

# defining a set of variables that we can use to internally specify our error types
BAD_ROLL_INPUT = "BAD_ROLL_INPUT"
INPUT_NOT_NUMBER = "INPUT_NOT_NUMBER"
NO_INPUT = "BAD_INPUT"

# Single function that generates a random number according to specified parameters
# and returns a built speechlet response
def roll_dice_handler(intent):
    """
    Given an intent for a dice roll, returns an Alexa readable response that describes the result
    of rolling dice with the given user specifications
    """
    # switching the intent over to the slots so we can pull our input values out
    intent = intent["slots"]

    # Pulling the dice and sides values (which are in all rolling intents)
    # Note, we have to coerce these values into ints because they are stored as strings
    num_dice, num_sides = int(intent["numDice"]["value"]), int(intent["numSides"]["value"])
    roll_value, modifier = 0, 0

    # Calculating a modifier if one has been specified by the user
    if "adding" in intent:
        modifier = modifier_to_number(intent["adding"]["value"], int(intent["modifier"]["value"]))

    # Calculating the value of the dice roll
    roll_value = roll_dice(num_dice, num_sides, modifier)

    # no session attributes necessary (maybe this will be changed later)
    session_attributes = {}

    # does not prompt the user for a response after making their call
    # (this might be changed later to allow the user to easily repeat a single roll_dice)
    should_end_session = True

    # Constructing a response string that describes the dice roll result
    res_str = create_result_string(roll_value)

    # the title of the card that appears in the alexa phone app
    card_title = "Dice Roll"

    # Note: we do not set a reprompt_text because in most use cases, the user
    # will only want to roll one dice at a time (hence, should_end_session is True)
    sp_res = build_speechlet_response(card_title, res_str, session_attributes, should_end_session)
    return build_response(session_attributes, sp_res)

def roll_dice(num_dice, num_sides, modifier=0):
    """
    Given a number of dice, the number of sides they have, and some modifier, return an integer
    which represents the total value of the completed roll
    """
    # double checking to see if bad input "slipped through the cracks"
    # the functions that grab these numbers from the intent should adequately trap though
    if (not isinstance(num_dice, int)) or (not isinstance(num_sides, int)) or (not isinstance(modifier, int)):
        return BAD_ROLL_INPUT
    # Note: we don't add modifier to the randint range because it is only added once
    my_sum = modifier

    for _ in range(0, num_dice):
        my_sum += randint(1, num_sides)

    return my_sum


def modifier_to_number(modifier_type, modifier_value):
    """
    Takes in the user input for modifier type / value, and returns a integer modifier_to_number

    This method handles error trapping for no input and bad input
    If no modifier type is given, the program will assume the user wants to add.
    """
    # here we define a set of possible words the user could input to specify addding / subtracting
    pos_mod_vals = ["adding", "add", "plus"]
    neg_mod_vals = ["subtract", "sub", "minus"]

    if modifier_type in pos_mod_vals:
        return modifier_value
    elif modifier_type in neg_mod_vals:
        return 0 - modifier_value
    else: # default case kept to clarify that ambiguous answers should be added by default
        return modifier_value

# Generates a user-readable string from a dice roll result
def create_result_string(roll_value):
    """
    Returns a basic string about a roll of roll_value that Alexa will read to the user.
    """
    return "Your roll is " + str(roll_value)


def get_dice_from_intent(intent):
    """
    First checks to see if each slot appears in the intent. If so, calls process_num to get an int
    Returns the three values in order
    """
    num_dice, num_sides, modifier = NO_INPUT, NO_INPUT, NO_INPUT

    if "numDice" in intent:
        num_dice = process_num(intent["numDice"]["value"])
    
    if "numSides" in intent:
        num_sides = process_num(intent["numSides"]["value"])
    
    # this is really the only case that needs checking on a proper call
    if "modifier" in intent:
        modifier = process_num(intent["modifier"]["value"])
    
    return num_dice, num_sides, modifier

# method to convert an intent value into an integer, and trap errors
def process_num(num):
    """
    Attempts to convert the provided num (as a string) into an integer
    if the input is "?" (what Alexa passes if there is no input), return NO_INPUT
    if the input errors when attempting to convert to an intger, return INPUT_NOT_NUMBER
    otherwise, return the number converted to an int
    """
    if num != "?" and num != None:
        try:
            num = int(num)
        except ValueError:
            return INPUT_NOT_NUMBER
        return num
    return NO_INPUT
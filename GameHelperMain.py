# Note, remove the shebang before uploading to AWS
"""
RPG Helper Logic code
For use on Amazon's Lambda AWS service with Alexa Skill "RPG Helper" only

Developed by Zac Patel on 1/10/17

Created using template: Alexa Skills Blueprint for Python 2.7
"""
# import for default (amazon) behavior
from __future__ import print_function
# import for logic (only importing randint function to save memory)
from random import randint

from SpeechHelpers import build_speechlet_response, build_response
from RiskLogic import RiskBattleHandler, RiskProbabilityHandler
# --------------- Functions that control the skill's behavior ------------------
# Note: I specify a default value for numDice, but Alexa's voice processing shouldEndSession
# always give us a value here (since it turns 'a' to 1)
def roll_dice(numDice, numSides, modifier=0):
    # Note: we don't add modifier to the randint range because it is only added once
    mysum = modifier
    for _ in range(0, numDice):
        mysum += randint(0, numSides)
    return mysum


def modifier_to_number(modifierType, modifierValue):
    # list of possible values that define the "sign" of the modifier
    # note we handle them in here because
    positiveModifierValues = {"adding, add, plus"}
    negativeModifierValues = {"subtract", "sub", "minus"}
    if modifierType in positiveModifierValues:
        return modifierValue
    elif modifierType in negativeModifierValues:
        return 0 - modifierValue
    else: # default case kept to clarify that ambiguous answers should be added by default
        return modifierValue

# Generates a user-readable string from a dice roll result
def create_result_string(rollValue, profileName="",):
    if profileName == "":
        return "Your roll is " + str(rollValue)
    else:
        return "The roll from " + profileName + " is " + str(rollValue)

# Single function that generates a random number according to specified parameters
# and returns a built speechlet response
def roll_dice_intent_handler(intentSlots, profileName=""):
    # Pulling the dice and sides values (which are in all rolling intents)
    # Note, we have to coerce these values into ints because they are stored as strings
    numDice, numSides = int(intentSlots["numDice"]["value"]), int(intentSlots["numSides"]["value"])
    rollValue, modifier = 0, 0

    # Calculating a modifier if one has been specified by the user
    if "adding" in intentSlots:
        modifier = modifier_to_number(intentSlots["adding"]["value"], int(intentSlots["modifier"]["value"]))

    # Calculating the value of the dice roll
    rollValue = roll_dice(numDice, numSides, modifier)

    session_attributes = {}

    # Constructing a response string that describes the dice roll result
    resultString = create_result_string(rollValue, profileName)

    # the title of the card that appears in the alexa phone app
    card_title = "Dice Roll"

    # Note: we do not set a reprompt_text because in most use cases, the user
    # will only want to roll one dice at a time (hence, should_end_session is True)
    return build_response(session_attributes,
        build_speechlet_response(card_title, resultString, None, True))


# TODO: build a method that goes into user stored data, grabs the dice profile
# that has been requested, and turns adds that data to the intent (so it can be
# passed into the rollDiceIntentHandler)


# Event Handler Methods
def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Wlecome to RPG Helper. What can I help you with?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Can I help you with your game?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using RPG Helper. "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------
# Note to Self: These are the 4 different types of interactions that the user

def on_session_started(session_started_request, session):
    """ Called when the session starts (every time the skill is run)"""

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

# note, intent_request is event["request"] and session is event["session"]
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    # Pulling data from the JSON vector
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Selecting different behavior for different intent types
    if intent_name == "RollDiceIntent":
        return roll_dice_intent_handler(intent["slots"])
    elif intent_name == "RollDiceWithModifierIntent":
        return roll_dice_intent_handler(intent["slots"])
    elif intent_name == "SimulateRiskBattleIntent":
        return RiskBattleHandler(intent["slots"])
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------
# Note: this is the one that is specified during the online setup of the lambda function
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    #TODO
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

"""
Game Helper Main Logic code
For use on Amazon's Lambda AWS service with Alexa Skill "Game Helper" only
This file is meant to tie all the individual function sets together, and handle their interface
with Alexa.

Developed by Zac Patel on 1/10/17

Created using template: Alexa Skills Blueprint for Python 2.7
"""
# import for default (amazon) behavior
from __future__ import print_function

# here we import only the function handler methods to make the code more modular and easy to read
# each "handler" type method should take in only an intent, and return a completed response
from SpeechHelpers import build_speechlet_response, build_response
from RiskLogic import battle_handler, battle_probability_handler
from DiceLogic import roll_dice_handler

#from WordHelper import word_value_handler, word_checker_handler, word_spell_handle

# Code version number: (so it can be accessed from other files easily)
VERSION = "A"

# Event Handler Methods
def get_welcome_response():
    """
    Called if the user starts a session without specifying an intent
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = """
    Welcome to Game Helper.
    I can help you generate dice rolls of any number of dice, of any number of sides, while optionally adding a modifier to the roll.
    I can also simulate battles of any number of attackers versus any number of defenders.
    Finally, I can calculate the probability of winning a battle of 2 to 12 attackers versus 1 to 11 attackers.
    Go ahead and ask me to roll dice, simulate battles, or calculate probabilities of winning.
    """

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Can I help you with your game?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
    """
    Called if the user requests help
    """
    session_attributes = {}
    card_title = "Help"
    speech_output = """
    I can help you generate dice rolls of any number of dice, of any number of sides, while optionally adding a modifier to the roll.
    For example, you can say, roll me 5 die 6 plus 4.
    I can also help simulate board game battle results similar to the game Risk.
    I have two capabilities in this area.
    First, I can simulate battles of any number of attackers versus any number of defenders.
    For example, you can say, simulate 5 attackers versus 4 defenders.
    Second, I can also calculate the probability of winning a battle of 2 to 12 attackers versus 1 to 11 attackers.
    For example, you can say, find the probability of 10 attackers beating 7 defenders. 
    """

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Can I help you with your game?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    """
    Called when the user tries to cancel or stop the current session
    """
    card_title = "Session Ended"
    speech_output = "Thank you for using Game Helper."

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
    if intent_name == "ROLLDICEINTENT":
        return roll_dice_handler(intent)
    elif intent_name == "SIMULATEBATTLEINTENT":
        return battle_handler(intent)
    elif intent_name == "CALCULATEPROBABILITYINTENT":
        return battle_probability_handler(intent)
    # Amazon's built in intent types below:
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
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

    # Application ID added to prevent calls 
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.9776484c-e52b-472a-928d-e4c982ea7d78"):
         raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

"""
AWS Alexa speech helper functions

Developed by Zac Patel on 1/10/17

Created using template: Alexa Skills Blueprint for Python 2.7
"""
# reading the version from the main file so it is easier to update
from GameHelperMain import VERSION

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Standard Alexa function (taken from template) that takes in the elements of a proper Alexa
    reponse, and returns a constructud JSON file to the user.
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """
    Standard Alexa function (taken from template) that takes in a speechlet response and the
    necessary session attributes and returns the finished JSON that Alexa will read out to the user
    """
    return {
        'version': VERSION,
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }



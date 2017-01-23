"""
Logic for the Scrabble helper functions of the Game Helper Alexa Skill

Developed by Zac Patel on 1/17/17
"""
# importing methods for creating final, Alexa readable responses
from GameHelperMain import build_speechlet_response, build_response

# Contains the scrabble point value of each letter
# Taken from wordfind.com (though this should be a standard chart)
letterValues = {'a':1, 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j': 8,  'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

# Returns the scrabble value of a word
def scrabbleValueHandler(intent):
    # Reading the user input word from the intent, and checking its value
    wordValue = getWordValue(getWordFromIntent(intent))

    


# returns the scrabble value of a word
def getWordValue(word):
    return sum([letterValues[letter] for letter in word])

def getWordFromIntent(intent):
    return intent["word"]["value"]
# find an api to run this section -> don't want to have a full english dictionary in the program...

# checks if a word given by the user is a valid scrabble word
def scrabbleWordCheckerHandler(intent):
    return

# checks if a word in some dictionary (figure this out later)
# probably use some dictionary.com api or something idk
def isWord(word):
    return
"""
    {
      "intent": "IsScrabbleWordIntent",
      "slots": [
        "name": "word",
        "type": "WORD"
      ]
    },

IsScrabbleWordIntent is {word} valid in scrabble
IsScrabbleWordIntent is {word} a valid scrabble word
IsScrabbleWordIntent is {word} usable in scrabble
IsScrabbleWordIntent is {word} playable in scrabble
IsScrabbleWordIntent is {word} a valid play in scrabble
IsScrabbleWordIntent can I play {word} in scrabble
IsScrabbleWordIntent can {word} be played in scrabble
IsScrabbleWordIntent can I use {word} in scrabble
IsScrabbleWordIntent can {word} be used in scrabble

"""
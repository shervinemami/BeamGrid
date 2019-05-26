# coding: utf-8
# A few handy functions for using mouse grids.
# By Shervin Emami (www.shervinemami.info), 2019.


import operator
from collections import OrderedDict     # Allows ordered dictionaries even in Python 2
from datetime import datetime

# Our symbols are spread across multiple files.
# Import the "letterMap" and similar dictionaries from the "lettermap.py" and similar files that are in the MacroSystem folder.
from lettermap import letterMap
from symbolmap import symbolMap1
from symbolmap import symbolMap2
from punctuationmap import punctuationMap1
from punctuationmap import punctuationMap2


# Set the mouse button actions here, to be used in multiple places in grammars
mouseActions = {
    "kick": 1,      # Left mouseclick
    "middle": 2,    # Middle mouseclick
    "psychic": 3,   # Right mouseclick
    "high": 4,      # Mouse wheel up
    "low": 5,       # Mouse wheel down
    "drag": 6,      # Left mousedown
    "release": 7,   # Left mouseup + Middle mouseup + Right mouseup
    "scroll": 8,    # Middle mousedown
    "double": 9,    # Double-click left mouse button
    "triple": 10,   # Triple-click left mouse button
}


# Create an ordered dictionary of all the symbols and phrases we might use in our mouse grids.
# Symbols that are easier to use should be placed near the top of the list, since some screens won't need to show the symbols on the bottom of the list.
def loadAllSymbols(keyboardMode):
    print
    print datetime.now(), "Loading all symbols. keyboardMode is", keyboardMode
    charsDict = OrderedDict()

    #for c in charsStart:
    #   charsDict[c] = c
    #print letterMap

    # Add all the numbers first
    for n in range(10):
        charsDict[str(n)] = str(n)

    # Then add the English alphabet, using the letter mapping phrases I've stored in letterMap.
    # Sort the letters first, since dictionaries in Python 2 aren't sorted.
    sorted_letters = sorted(letterMap.items(), key=operator.itemgetter(1))
    for key, val in sorted_letters:
        #print u"(", key, u", ", val
        charsDict[key] = val

    # Then add some extra symbols that are on keyboards and are a single word (thus can be easy to say, and allows more symbols for mouse grid modes):
    for key, val in punctuationMap1.iteritems():
        charsDict[key] = val

    # Then add many extra Unicode symbols that aren't on keyboards but are a single word (thus can be easy to say, and allows more symbols for mouse grid modes):
    if not keyboardMode:
        for key, val in symbolMap1.iteritems():
            charsDict[key] = val

    # Then add the harder symbols that are on keyboards and might not be a single word:
    for key, val in punctuationMap2.iteritems():
        charsDict[key] = val

    # Then add the harder Unicode symbols that aren't on keyboards and might not be a single word:
    if not keyboardMode:
        for key, val in symbolMap2.iteritems():
            charsDict[key] = val

    #print charsDict
    return charsDict

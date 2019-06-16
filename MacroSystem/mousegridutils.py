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
from symbolmap import symbolMap3
from punctuationmap import punctuationMap1
from punctuationmap import punctuationMap2


# Set the mouse button actions here, to be used in multiple places in grammars
mouseActions = {
    "kick":                1,  # Left mouseclick
    "middle":              2,  # Middle mouseclick
    "psychic":             3,  # Right mouseclick
    "high":                4,  # Mouse wheel up
    "low":                 5,  # Mouse wheel down
    "drag-mouse":          6,  # Left mousedown. "drag" sounds like "right", so it's better to say "drag-mouse"
    "release":             7,  # Left mouseup + Middle mouseup + Right mouseup
    "scroll":              8,  # Middle mousedown
    "double":              9,  # Double-click left mouse button
    "triple":             10,  # Triple-click left mouse button
    "control-kick":       11,  # Hold down Control key while clicking the left mouse button
    "shift-kick":         12,  # Hold down Shift key while clicking the left mouse button
    "alt-kick":           13,  # Hold down Alt key while clicking the left mouse button
    "control-drag-mouse": 14,  # Hold down Control key while dragging with the left mouse button
    "shift-drag-mouse":   15,  # Hold down Shift key while dragging with the left mouse button
    "alt-drag-mouse":     16,  # Hold down Alt key while dragging with the left mouse button
    "control-psychic":    17,  # Hold down Control key while clicking the right mouse button
    "shift-psychic":      18,  # Hold down Shift key while clicking the right mouse button
    "alt-psychic":        19,  # Hold down Alt key while clicking the right mouse button
}


# Just a few generic dictionaries of the numbers that are likely to be used for fairly large sizes and repetition counts
smallNumbers = {
    "zero":                           0,
    "one":                            1,
    "two":                            2,
    "three":                          3,
    "four":                           4,
    "five":                           5,
    "six":                            6,
    "seven":                          7,
    "eight":                          8,
    "nine":                           9,
    "ten":                           10,
    "eleven":                        11,
    "twelve":                        12,
    "thirteen":                      13,
    "fourteen":                      14,
    "fifteen":                       15,
    "sixteen":                       16,
    "seventeen":                     17,
    "eighteen":                      18,
    "nineteen":                      19,
    "twenty":                        20,
    "twenty-one":                    21,
    "twenty-two":                    22,
    "twenty-three":                  23,
    "twenty-four":                   24,
    "twenty-five":                   25,
    "twenty-six":                    26,
    "twenty-eight":                  28,
    "thirty":                        30,
    "thirty-one":                    31,
    "thirty-two":                    32,
    "thirty-five":                   35,
    "thirty-six":                    36,
    "thirty-eight":                  38,
    "forty":                         40,
    "forty-two":                     42,
    "forty-five":                    45,
    "fifty":                         50,
}

bigNumbers = {
    "fifty-five":                    55,
    "sixty":                         60,
    "sixty-five":                    65,
    "seventy":                       70,
    "seventy-five":                  75,
    "eighty":                        80,
    "eighty-five":                   85,
    "ninety":                        90,
    "ninety-five":                   95,
    "ninety-nine":                   99,
    "one-hundred":                  100,
    "one-hundred-and-ten":          110,
    "one-hundred-and-fifteen":      115,
    "one-hundred-and-twenty":       120,
    "one-hundred-and-twenty five":  125,
    "one-hundred-and-thirty":       130,
    "one-hundred-and-forty":        140,
    "one-hundred-and-fifty":        150,
    "one-hundred-and-sixty":        160,
    "one-hundred-and-seventy":      170,
    "one-hundred-and-seventy five": 175,
    "one-hundred-and-eighty":       180,
    "one-hundred-and-ninety":       190,
    "two-hundred":                  200,
    "two-hundred-and-twenty five":  225,
    "two-hundred-and-fifty":        250,
    "two-hundred-and-seventy five": 275,
    "three-hundred":                300,
    "three-hundred-and-fifty":      350,
    "four-hundred":                 400,
    "four-hundred-and-fifty":       450,
    "five-hundred":                 500,
    "five-hundred-and-fifty":       550,
    "six-hundred":                  600,
    "six-hundred-and-fifty":        650,
    "seven-hundred":                700,
    "seven-hundred-and-fifty":      750,
    "eight-hundred":                800,
    "eight-hundred-and-fifty":      850,
    "nine-hundred":                 900,
    "nine-hundred-and-fifty":       950,
    "one-thousand":                1000,
    "one-thousand-five-hundred":   1500,
    "two-thousand":                2000,
}

# Create a combination of small and big numbers
mostNumbers = smallNumbers.copy()
mostNumbers.update(bigNumbers)    # merge both dictionaries



# Create an ordered dictionary of all the symbols and phrases we might use in our mouse grids.
# Symbols that are easier to use should be placed near the top of the list, since some screens won't need to show the symbols on the bottom of the list.
def loadAllSymbols(keyboardMode, extendedSymbolsLevel = 1, extendedSymbolsCount = 9999999):
    print datetime.now(), "Loading all symbols up to level", extendedSymbolsLevel, ", count", extendedSymbolsCount, ". keyboardMode is", keyboardMode, ".",
    charsDict = OrderedDict()

    #for c in charsStart:
    #   charsDict[c] = c
    #print letterMap

    # Make sure we don't load more symbols than what is asked
    c = 0
    
    # Add all the numbers first
    for n in range(10):
        if c < extendedSymbolsCount:
            c += 1
            charsDict[str(n)] = str(n)

    # Then add the English alphabet, using the letter mapping phrases I've stored in letterMap.
    # Sort the letters first, since dictionaries in Python 2 aren't sorted.
    #print "letterMap:", letterMap
    sorted_letters = sorted(letterMap.items(), key=operator.itemgetter(1))
    for key, val in sorted_letters:
        if c < extendedSymbolsCount:
            c += 1
            #print u"(", key, u", ", val
            charsDict[key] = val

    # Then add some extra symbols that are on keyboards and are a single word (thus can be easy to say, and allows more symbols for mouse grid modes):
    for key, val in punctuationMap1.iteritems():
        if c < extendedSymbolsCount:
            c += 1
            charsDict[key] = val

    # Then add many extra Unicode symbols that aren't on keyboards but are a single word (thus can be easy to say, and allows more symbols for mouse grid modes):
    if not keyboardMode:
        for key, val in symbolMap1.iteritems():
            if c < extendedSymbolsCount:
                c += 1
                charsDict[key] = val

    # Then add the slightly harder Unicode symbols that aren't on keyboards:
    if not keyboardMode and extendedSymbolsLevel >= 2:
        for key, val in symbolMap2.iteritems():
            if c < extendedSymbolsCount:
                c += 1
                charsDict[key] = val

    # Then add the harder symbols that are on keyboards and might not be a single word:
    for key, val in punctuationMap2.iteritems():
        if c < extendedSymbolsCount:
            c += 1
            charsDict[key] = val

    # Then add the harder Unicode symbols that aren't on keyboards and might not be a single word:
    if not keyboardMode and extendedSymbolsLevel >= 3:
        for key, val in symbolMap3.iteritems():
            if c < extendedSymbolsCount:
                c += 1
                charsDict[key] = val

    #print charsDict
    print "Loaded", len(charsDict), "symbols."
    return charsDict

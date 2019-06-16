# Mouse clicks that can be performed at anytime, by voice on a possibly remote machine and different OS, through Aenea.
# This is being used with "_all.py" so that grammars can include a mouse button action at the end of a sequence of phrases.
# By Shervin Emami (www.shervinemami.info), 2019.

from mousegridutils import mouseActions
from mousegridutils import smallNumbers
import time

from aenea import (
    Grammar,
    MappingRule,
    Text,
    Key,
    Mimic,
    Function,
    Dictation,
    Choice,
    Window,
    Config,
    Section,
    Item,
    IntegerRef,
    Alternative,
    RuleRef,
    Repetition,
    CompoundRule,
    AppContext,
)

# Allow calling aenea server-side plugins
try:
    import aenea.communications
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise


# Saying "kick" will click the left mouse button wherever the mouse cursor currently is.
class MouseButtonRule(CompoundRule):
    spec = "<mouseAction> [<repetitions>]"
    extras = [
        Choice("mouseAction", mouseActions),
        Choice("repetitions", smallNumbers),
    ]
    defaults = {"repetitions": 1}

    def value(self, node):
        # This file is imported by "_all.py" and needs to return something that has an "execute()" function.
        # But remote mouse actions don't have an "execute()" function, and if we directly perform mouse actions here,
        # they will get executed before the rest of the actions.
        # To support our mouse grid modes, we want the mouse action to happen at the end of the sequence, so the
        # user can move the mouse cursor first then click the mouse after the move.
        # So we'll do nothing in "value()", but we'll get "_all.py" to call "possibleMouseAction()" at the end of
        # the sequence.
        #print "MouseButtonRule is saving the words", node.words(), "to check for mouse button actions later."
        #self.words = node.words()
        return Text()


def possibleMouseAction(words):
    # Search for a mouse button action, starting from the right-most word
    print "Testing mouse action in", words
    action = -1
    index = -1
    word = ""
    # Check the last word for an action
    try:
        index = len(words)-1
        word = words[index]
        action = mouseActions[word]
    except:
        pass
    # Check the 2nd last word for an action
    try:
        index = len(words)-2
        word = words[index]
        action = mouseActions[word]
    except:
        pass

    # Find the repetition count
    repetitions = 1
    try:
        # Grab all words to the right of the mouse action word
        repetition_string = words[index+1:][0]
        repetitions = smallNumbers[repetition_string]
    except:
        pass

    #print "Calling showMouseGrid(-1) on the server to hide the MouseGrid"
    ## Run our aenea plugin script that shows the mouse grid fullscreen in Linux.
    #aenea.communications.server.showMouseGrid(-1)

    # Control the mouse
    if action >= 0 and repetitions >= 1:
        print "Calling clickMouseGrid(%d) on the server %d times" % (action, repetitions)
        # Run our aenea plugin script that moves and clicks the mouse in Linux.
        for i in range(repetitions):
            pid = aenea.communications.server.clickMouseGrid(action)
            time.sleep(0.01)

    # Majority of the time, there won't be any mouse actions being spoken and therefore
    # most of the time it will come here.

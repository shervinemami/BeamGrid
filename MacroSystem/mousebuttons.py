# Mouse clicks that can be performed at anytime, by voice on a possibly remote machine and different OS, through Aenea.
# This is being used with "_all.py" so that grammars can include a mouse button action at the end of a sequence of phrases.
# By Shervin Emami (www.shervinemami.info), 2019.

from mousegridutils import mouseActions

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
    spec = "<mouseAction>"
    extras = [
        Choice("mouseAction", mouseActions),
    ]

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
    # Check if the last word spoken is a mouse button action
    try:
        print "Testing mouse action in", words
        action = mouseActions[words[len(words)-1]]

        #print "Calling showMouseGrid(-1) on the server to hide the MouseGrid"
        ## Run our aenea plugin script that shows the mouse grid fullscreen in Linux.
        #aenea.communications.server.showMouseGrid(-1)

        # Control the mouse
        button_int = int(action)
        print "Calling clickMouseGrid(%d) on the server" % (button_int)
        # Run our aenea plugin script that moves and clicks the mouse in Linux.
        pid = aenea.communications.server.clickMouseGrid(button_int)
        #print "Returned pid", pid

    except:
        # Majority of the time, there won't be any mouse actions being spoken and therefore
        # most of the time it will come here.
        pass

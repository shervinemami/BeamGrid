# _all.py: main rule for DWK's grammar

from natlink import setMicState
from aenea import *

# Allow calling aenea plugins
try:
    import aenea.communications
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise


import keyboard
import words
import programs

import mousebuttons

release = Key("shift:up, ctrl:up, alt:up")

alternatives = []
alternatives.append(RuleRef(rule=keyboard.KeystrokeRule()))
alternatives.append(RuleRef(rule=words.FormatRule()))
#alternatives.append(RuleRef(rule=words.ReFormatRule()))
alternatives.append(RuleRef(rule=words.NopeFormatRule()))
alternatives.append(RuleRef(rule=programs.ProgramsRule()))
alternatives.append(RuleRef(rule=mousebuttons.MouseButtonRule()))

root_action = Alternative(alternatives)

# Note: The value you set in "max" here is the most number of commands you can give between a pause.
sequence = Repetition(root_action, min=1, max=25, name="sequence")


class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [repeat that <n> times]"
    extras = [
        sequence,  # Sequence of actions defined above.
        IntegerRef("n", 1, 101),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        count = extras["n"]  # An integer repeat count.
        print "In RepeatRule", sequence
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()
            release.execute()

        words = node.words()
        print "In RepeatRule. spoken words:", words
        
        # Now that the main actions have been executed, check if there is a mouse action waiting to execute
        mousebuttons.possibleMouseAction(words)


# This grammar is our main root grammar that we want to apply at all times, except when the mouse grid (invisible window) is open
invisibleMouseWindowContext = ProxyAppContext(title="InvisibleWindow - ")
notInvisibleMouseWindowContext = ~invisibleMouseWindowContext
grammar = Grammar("root rule", context=notInvisibleMouseWindowContext)
#grammar = Grammar("root rule")
grammar.add_rule(RepeatRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.

def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

# module for dictating words and basic sentences
#
# (based on the multiedit module from dragonfly-modules project)
# (heavily modified)
# (the original copyright notice is reproduced below)
#
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

import aenea
import aenea.misc
import aenea.vocabulary
import aenea.configuration
import aenea.format

from aenea import (
    AeneaContext,
    AppContext,
    Alternative,
    CompoundRule,
    Dictation,
    DictList,
    DictListRef,
    Grammar,
    IntegerRef,
    Literal,
    ProxyAppContext,
    MappingRule,
    NeverContext,
    Repetition,
    RuleRef,
    Sequence
)

from aenea import (
    Key,
    Text
)

lastFormatRuleLength = 0
lastFormatRuleWords = []

class NopeFormatRule(CompoundRule):
    spec = ('undo that')

    def value(self, node):
        global lastFormatRuleLength
        print "erasing previous format of length", lastFormatRuleLength
        return Key('backspace:' + str(lastFormatRuleLength))

#class ReFormatRule(CompoundRule):
#    spec = ('that was [upper | natural] ( proper | camel | rel-path | abs-path | score | sentence | '
#            'scope-resolve | jumble | dotword | dashword | natword | snakeword | brooding-narrative)')
#
#    def value(self, node):
#        global lastFormatRuleWords
#        words = lastFormatRuleWords
#        words = node.words()[2:] + lastFormatRuleWords
#        print words
#
#        uppercase = words[0] == 'upper'
#        lowercase = words[0] != 'natural'
#
#        if lowercase:
#            words = [word.lower() for word in words]
#        if uppercase:
#            words = [word.upper() for word in words]
#
#        words = [word.split('\\', 1)[0].replace('-', '') for word in words]
#        if words[0].lower() in ('upper', 'natural'):
#            del words[0]
#
#        function = getattr(aenea.format, 'format_%s' % words[0].lower())
#        formatted = function(words[1:])
#
#        global lastFormatRuleLength
#        lastFormatRuleLength = len(formatted)
#        return Text(formatted)

class FormatRule(CompoundRule):
    # I significantly reduced the formatting options, since I rarely use most of them, and they kept being accidentally picked up.
    # "macro" means "upper score", such as "HELLO_WORLD".
    # "without spaces" means "jumble", such as "helloworld", since "jumble" sounds like "jump" that is used in my grammar.
    # "cat" means "natword", such as "hello world"
    # I also moved "upper" into the individual formatting rule, and made <dictation> necessary, so they get randomly picked up less often.
    #spec = ('[upper | natural] ( proper | camel | rel-path | abs-path | score | sentence | '
    #        'scope-resolve | jumble | dotword | dashword | natword | snakeword | brooding-narrative) [<dictation>] [bomb]')
    spec = ('( proper | camel | macro | sentence | [uppercase] without spaces | [uppercase] (natword | cat) ) <dictation> [bomb]')
    extras = [Dictation(name='dictation')]

    def value(self, node):
        words = node.words()
        print "format rule:", words

        #-------------------------------------------
        # Handle uppercase
        uppercase = words[0] == 'uppercase'
        #lowercase = words[0] != 'natural'

        #if lowercase:
        #    words = [word.lower() for word in words]
        if uppercase:
            words = [word.upper() for word in words]

        words = [word.split('\\', 1)[0].replace('-', '') for word in words]
        if words[0].lower() in ('uppercase', 'natural'):
            del words[0]

        #-------------------------------------------
        # Handle 'without spaces'
        if 'without' in words[0] and 'spaces' in words[1]:
            # Use jumble mode
            words[0] = 'jumble'
            # Get rid of the "spaces" word
            del words[1]

        #-------------------------------------------
        # Handle 'macro'
        if 'macro' in words[0]:
            # Get macro to use underscore_formatting_mode
            words[0] = 'score'
            # Convert all the words to UPPERCASE
            words = [word.upper() for word in words]

        #-------------------------------------------
        # Handle 'cat'
        if 'cat' in words[0]:
            # Simply replace 'cat' with 'natword'
            words[0] = 'natword'

        #-------------------------------------------
        # Handle 'bomb'
        bomb = None
        if 'bomb' in words:
            bomb_point = words.index('bomb')
            if bomb_point+1 < len(words):
                bomb = words[bomb_point+1 : ]
            words = words[ : bomb_point]


        #-------------------------------------------
        # Process all the words
        function = getattr(aenea.format, 'format_%s' % words[0].lower())
        formatted = function(words[1:])
        global lastFormatRuleWords
        lastFormatRuleWords = words[1:]

        global lastFormatRuleLength
        lastFormatRuleLength = len(formatted)

        # empty formatted causes problems here
        print "  ->", formatted
        if bomb != None:
            return Text(formatted) + Mimic(' '.join(bomb))
        else:
            return Text(formatted)


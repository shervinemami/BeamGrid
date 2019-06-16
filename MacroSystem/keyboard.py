# Low-level keyboard input module
# Words that are recommend to manually train Dragon with:
#   !      exclamationmark     (sometimes Dragon has trouble with the short space between words when I say "exclamation mark")
#   ?      questionmark        (sometimes Dragon has trouble with the short space between words when I say "question mark")
#   krife
#   osez
#   yeelax
#   zimeesi
#
#
# Based on the work done by the creators of the Dictation Toolbox
# https://github.com/dictation-toolbox/dragonfly-scripts
#
# and _multiedit-en.py found at:
# http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html
#
# Modifications by: Tony Grosinger and Shervin Emami.
#
# Licensed under LGPL

from natlink import setMicState
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

from lettermap import letterMap
import copy

from dragonfly.actions.keyboard import keyboard
from dragonfly.actions.typeables import typeables
if 'semicolon' not in typeables:
    typeables["semicolon"] = keyboard.get_typeable(char=';')


#  Note that this doesn't include the less common keys such as the "window" key.
release = Key("shift:up, ctrl:up, alt:up")


def cancel_and_sleep(text=None, text2=None):
    """Used to cancel an ongoing dictation and puts microphone to sleep.

    This method notifies the user that the dictation was in fact canceled,
     a message in the Natlink feedback window.
    Then the the microphone is put to sleep.
    Example:
    "'random mumbling go to sleep'" => Microphone sleep.

    """
    print("* Dictation canceled. Going to sleep. *")
    setMicState("sleeping")


# For repeating of characters.
specialCharMap = {
    "pipe": "|",
    "minus": "-",
    "dot": ".",
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(asterisk|Asterix)": "*",
    "colon": ":",
    "(semicolon|semi-colon)": ";",
    "at symbol": "@",
    #"[double] quote": '"',
    "quotes": '"',
    "single quote": "'",
    "apostrophe": "'",
    "hash": "#",
    "dollar sign": "$",
    "percentage": "%",
    "ampersand": "&",
    "slash": "/",
    "equals": "=",
    "plus": "+",
    "space": " ",
    "exclamationmark": "!",		# "bang" sounds like "aim" that I might use for "a"
	#"bang": "!",
    "questionmark": "?",
    "caret": "^",
	"tilde": "~",
	"back tick": "`",
    

    # some other symbols I haven't imported yet, lazy sorry
    # 'ampersand': Key('ampersand'),
    # 'apostrophe': Key('apostrophe'),
    # 'asterisk': Key('asterisk'),
    # 'at': Key('at'),
    # 'backslash': Key('backslash'),
    # 'backtick': Key('backtick'),
    # 'bar': Key('bar'),
    # 'caret': Key('caret'),
    # 'colon': Key('colon'),
    # 'comma': Key('comma'),
    # 'dollar': Key('dollar'),
    # #'(dot|period)': Key('dot'),
    # 'double quote': Key('dquote'),
    # 'equal': Key('equal'),
    # 'bang': Key('exclamation'),
    # 'hash': Key('hash'),
    # 'hyphen': Key('hyphen'),
    # 'minus': Key('minus'),
    # 'percent': Key('percent'),
    # 'plus': Key('plus'),
    # 'question': Key('question'),
    # # Getting Invalid key name: 'semicolon'
    # #'semicolon': Key('semicolon'),
    # 'slash': Key('slash'),
    # '[single] quote': Key('squote'),
    # 'tilde': Key('tilde'),
    # 'underscore | score': Key('underscore'),
}

# All the keys that can be pressed with the Window key down.
#windowCharMap = {
#    "space": Key("space"),
#    "up": Key("up"),
#    "down": Key("down"),
#    "left": Key("left"),
#    "right": Key("right"),
#    "enter": Key("enter"),
#    "tab": Key("tab"),
#    "insert": Key("insert"),
#    "1": Text("1"),
#    "2": Text("2"),
#    "3": Text("3"),
#    "4": Text("4"),
#    "5": Text("5"),
#}


## Modifiers for the press-command.
#modifierMap = {
#    "alt": "a",
#    "control": "c",
#    "shift": "s",
#    "super": "w",
#}
#
## Modifiers for the press-command, if only the modifier is pressed.
#singleModifierMap = {
#    "alt": "alt",
#    "control": "ctrl",
#    "shift": "shift",
#    "super": "win",
#}

# letterMap = dictionary in separate "letterMap.py" file, so it can also be used by the "practice_mappings.py" tool.

# generate uppercase versions of every letter
upperLetterMap = {}
for letter in letterMap:
    upperLetterMap["maxo " + letter] = letterMap[letter].upper()         #
    #upperLetterMap["roof " + letter] = letterMap[letter].upper()         # My "roof zimeesi" fails
    #upperLetterMap["biggie " + letter] = letterMap[letter].upper()         # My "biggie" is like video
    #upperLetterMap["buzz " + letter] = letterMap[letter].upper()         # My "buzz" is like "plus"
    #upperLetterMap["fig " + letter] = letterMap[letter].upper()         # My "fig char" fails
    #upperLetterMap["gross " + letter] = letterMap[letter].upper()         # My "gross" is like "quotes"
    #upperLetterMap["bam " + letter] = letterMap[letter].upper()         # My "bam" is like "end"
    #upperLetterMap["big " + letter] = letterMap[letter].upper()         # My "big" is pretty good, but usually fails "big yeelax"
    #upperLetterMap["case " + letter] = letterMap[letter].upper()         # My "case" is too much like "plus"
    #upperLetterMap["capital " + letter] = letterMap[letter].upper()     # My "cap" is too much like "up"
    #upperLetterMap["sky " + letter] = letterMap[letter].upper()         # My "sky" is too much like "score" :-(

# Generate a dictionary containing both the lowercase and uppercase alphabet
letterMapBothCases = copy.deepcopy(letterMap)
letterMapBothCases.update(upperLetterMap)


def handle_word(text):
    #words = map(list, text)
    #print text
    words = str(text).split()
    print 'word (', words, ')'
    if len(words) > 0:
        Text(words[0]).execute()
        if len(words) > 1:
            Mimic(' '.join(words[1:])).execute()


grammarCfg = Config("multi edit")
grammarCfg.cmd = Section("Language section")
grammarCfg.cmd.map = Item(
    {
        # Navigation keys.
        "up [<n> times]": Key("up:%(n)d/10"),
        "down [<n> times]": Key("down:%(n)d/10"),
        "left [<n> times]": Key("left:%(n)d/10"),
        "right [<n> times]": Key("right:%(n)d/10"),
        "page up [<n> times]": Key("pgup:%(n)d"),
        "page down [<n> times]": Key("pgdown:%(n)d"),
        "jump [<n> times]": Key("pgup:%(n)d"),
        "drop [<n> times]": Key("pgdown:%(n)d"),
        "jump half": Key("up:30/10"),       # Half of a page up/down. When I say "jump half" quickly, Dragon hears it as a single word, so we also support that.
        "jumpuff": Key("up:30/10"),
        "drop half": Key("down:30/10"),
        "drohpuff": Key("down:30/10"),
        #"up <n> (page|pages)": Key("pgup:%(n)d"),
        #"down <n> (page|pages)": Key("pgdown:%(n)d"),
        #"left <n> (word|words)": Key("c-left/3:%(n)d/10"),
        #"right <n> (word|words)": Key("c-right/3:%(n)d/10"),
        "home": Key("home"),
        "end": Key("end"),
		"insert": Key("insert"),

		# Other special keys that could be nice to have, but might not be supported so far:
			#Caps_Lock
			#Alt_R
			#KP_Insert
			#Redo
			#XF86AudioPlay
			#XF86AudioNext
			#XF86AudioForward
			#XF86AudioPause
			#XF86AudioRaiseVolume
			#XF86AudioLowerVolume
			#XF86Back
			#KP_Next
			#Scroll_Lock
			#XF86MonBrightnessUp
			#XF86MonBrightnessDown
			#XF86ScrollUp
			#XF86ScrollDown
			#Insert
			#Next
			#XF86Next
			#XF86AudioMute
			#f1 ... f24
			#Print
			#Pause
        #"doc home": Key("c-home/3"),
        #"doc end": Key("c-end/3"),
        # Functional keys.
        #"space": release + Key("space"),
        "space [<n> times]": release + Key("space:%(n)d"),
        "(enter) [<n> times]": release + Key("enter:%(n)d"),
        "tab [<n> times]": Key("tab:%(n)d"),
        #"delete this line": Key("home, s-end, del"),  # @IgnorePep8
        "backspace [<n> times]": release + Key("backspace:%(n)d"),
        #"application key": release + Key("apps/3"),
        #"paste [that]": Function(paste_command),
        #"copy [that]": Function(copy_command),
        #"cut [that]": release + Key("c-x/3"),
        #"select all": release + Key("c-a/3"),
        #"[(hold|press)] met": Key("alt:down/3"),

        # Function keys. For some reason the functionKeyMap above isn't working for me.
        'F one': Key('f1'),
        'F two': Key('f2'),
        'F three': Key('f3'),
        'F four': Key('f4'),
        'F five': Key('f5'),
        'F six': Key('f6'),
        'F seven': Key('f7'),
        'F eight': Key('f8'),
        'F nine': Key('f9'),
        'F ten': Key('f10'),
        'F eleven': Key('f11'),
        'F twelve': Key('f12'),

        #"window": Key("win:down/3"),
        #"win key": release + Key("win/3"),
        #"window <windowChars>": Key("win:down") + Text("%(windowChars)s") + Key("win:up"),
        #"window run": Key("win:down/3") + Text("r") + Key("win:up"),
        #"release window": Key("win:up"),
        #"window [<num>]": Key("win:down/3") + Text("%(num)d") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 1": Key("win:down/3") + Text("1") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 2": Key("win:down/3") + Text("2") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 3": Key("win:down/3") + Text("3") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 4": Key("win:down/3") + Text("4") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 5": Key("win:down/3") + Text("5") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 6": Key("win:down/3") + Text("6") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 7": Key("win:down/3") + Text("7") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window space": Key("win:down") + Key("space")  + Key("win:up"),
        "window up":    Key("win:down") + Key("up")     + Key("win:up"),
        "window down":  Key("win:down") + Key("down")   + Key("win:up"),
        "window left":  Key("win:down") + Key("left")   + Key("win:up"),
        "window right": Key("win:down") + Key("right")  + Key("win:up"),
        "window enter": Key("win:down") + Key("enter")  + Key("win:up"),
        "window tab":   Key("win:down") + Key("tab")    + Key("win:up"),
        #"window tab":   Key("w-tab/30"),
        "window insert": Key("win:down") + Key("insert") + Key("win:up"),
        "window <letters>": Key("win:down") + Text("%(letters)s") + Key("win:up"),
        # Moved to _aenea.py
        #"window list":      Key("win:down/999, tab") + Key("win:up"),
        
        # Switch between Linux & Windows through the Synergy application
        "gravy": Key("ctrl:down/3") + Key("backtick") + Key("ctrl:up"),
        "porridge": Key("ctrl:down/3") + Key("tilde") + Key("ctrl:up"),

        "meta [<num>]": Key("alt:down/1") + Text("%(num)d") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
        #"meta tab": Key("a-tab/20"),
		#meta": Key("alt:down/3"),    # Or do I prefer "alter"?
		"meta 1": Key("alt:down/3") + Text("1") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 2": Key("alt:down/3") + Text("2") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 3": Key("alt:down/3") + Text("3") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 4": Key("alt:down/3") + Text("4") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 5": Key("alt:down/3") + Text("5") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 6": Key("alt:down/3") + Text("6") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 7": Key("alt:down/3") + Text("7") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		#"meta 8": Key("alt:down/3") + Text("8") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 9": Key("alt:down/3") + Text("9") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
        #"hold met": Key("alt:down/3"),
        #"release met": Key("alt:up"),

        # My current aenea proxy system isn't allowing to hold down shift or caps lock, so I'm using Linux AutoKey instead. See "programs.py"
        "shift": Key("shift:down/3"),
        #"hold shift": Key("shift:down"),
        #"release shift": Key("shift:up"),
        "control": Key("ctrl:down/3"),
        #"hold control": Key("ctrl:down"),
        #"release control": Key("ctrl:up"),
        "release all": Key("shift:up, ctrl:up, alt:up, win:up,  shift:down, shift:up, ctrl:down, ctrl:up, alt:down, alt:up, win:down, win:up"),
        #"press key <pressKey>": Key("%(pressKey)s"),

        # Closures.
        #"angle brackets": Key("langle, rangle, left/3"),
        #"[square] brackets": Key("lbracket, rbracket, left/3"),
        #"[curly] braces": Key("lbrace, rbrace, left/3"),
        #"(parens|parentheses)": Key("lparen, rparen, left/3"),
        #"quotes": Key("dquote/3, dquote/3, left/3"),
        #"backticks": Key("backtick:2, left"),
        #"single quotes": Key("squote, squote, left/3"),
        # Shorthand multiple characters.
        #"double <char>": Text("%(char)s%(char)s"),
        #"triple <char>": Text("%(char)s%(char)s%(char)s"),
        #"double escape": Key("escape, escape"),  # Exiting menus.
        # Punctuation and separation characters, for quick editing.
        "colon": Key("colon"),
        "semi-colon": Key("semicolon"),
        "comma": Key("comma"),
        "dot": Key("dot"),  # cannot be followed by a repeat count
        "dotdot": Key("dot") + Key("dot"),     # Added because Dragon often doesn't recognize my "dot dot dot" sequences
        "dotdotdot": Key("dot") + Key("dot") + Key("dot"),
        "full stop": Key("dot"),  # cannot be followed by a repeat count
        "point <digit> [<digit2>]": Key("dot") + Text("%(digit)d") + Text("%(digit2)d"),  # allow to say "number 1.23"
        "(dash|minus)": Key("hyphen"),
        "underscore": Key("underscore"),

        # These are needed by this grammar, otherwise many of these rules won't work!
        "<letters>": Text("%(letters)s"),
        "<char>": Text("%(char)s"),

        'less than': Key('langle'),     # angle bracket
		#'langle': Key('langle:%(n)d'),
        'curly brace':   Key('lbrace'),       # curly brace
        'square bracket':   Key('lbracket'),      # square bracket
        'round bracket':    Key('lparen'),        # round parenthesis
        'greater than': Key('rangle'),
		#'rangle': Key('rangle'),
        'close curly':   Key('rbrace'),
        'close square':   Key('rbracket'),
        'close round':   Key('rparen'),
        'close bracket':  Key('rparen'),    # Only included here because otherwise, it causes "Close Dragon"!

        "escape": Key("escape"),
        #"escape 2 ": Key("escape") + Key("escape"),
        "cancel": Key("escape"),

        'delete [<n> times]':       Key('del:%(n)d'),
		#'chuck [<n>]':       Key('del:%(n)d'),
        #'scratch [<n>]':     Key('backspace:%(n)d'),
		
        #"visual": Key("v"),
        #"visual line": Key("s-v"),
        #"visual block": Key("c-v"),
        #"doc save": Key("c-s"),
        #"(arrow|pointer)": Text("->"),

        #'fly [<n>]':  Key('pgup:%(n)d'),
        #'drop [<n>]':  Key('pgdown:%(n)d'),

        #'lope [<n>]':  Key('c-left:%(n)d'),
        #'(yope|rope) [<n>]':  Key('c-right:%(n)d'),
        #'(hill scratch|hatch) [<n>]': Key('c-backspace:%(n)d'),

        #'hexadecimal': Text("0x"),
        #'suspend': Key('c-z'),
		#'undo': Key('c-z'),  # Sounds too much like "end"
		"geez [<n> times]": Key('c-z:%(n)d'),

        #'word <text>': Function(handle_word),
        'number <num>': Text("%(num)d"),
        #'zero': Text("0"),  # Allowed to say "zero" instead of "number zero", since it's common to need many zeros
        '<digit>': Text("%(digit)d"),   # Allowed to say "zero" ... "nine" instead of "number zero" ..., since it's common to need a single digit
        #'change <text> to <text2>': Key("home, slash") + Text("%(text)s") + Key("enter, c, e") + Text("%(text2)s") + Key("escape"),

        # Text corrections.
        #"again": Key("ctrl:down/3, shift:down/3, left") + Key("ctrl:up, shift:up"), # Type over a word
        #"fix missing space": Key("c-left/3, space, c-right/3"),
        #"remove extra space": Key("c-left/3, backspace, c-right/3"),  # @IgnorePep8
        #"remove extra character": Key("c-left/3, del, c-right/3"),  # @IgnorePep8
        # Microphone sleep/cancel started dictation.
        #"[<text>] (go to sleep|cancel and sleep) [<text2>]": Function(cancel_and_sleep),  # @IgnorePep8
    },
    namespace={
        "Key": Key,
        "Text": Text,
    }
)


class KeystrokeRule(MappingRule):
    exported = False
    mapping = grammarCfg.cmd.map
    extras = [
        IntegerRef("n", 1, 101),
        IntegerRef("num", 0, 101),
        IntegerRef("digit", 0, 10),
        IntegerRef("digit2", 0, 10),
        Dictation("text"),
        #Dictation("text2"),
        Choice("char", specialCharMap),
        Choice("letters", letterMapBothCases),
        #Choice("modifier1", modifierMap),
        #Choice("modifier2", modifierMap),
        #Choice("modifierSingle", singleModifierMap),
        #Choice("windowChars", windowCharMap),
    ]
    defaults = {
        "n": 1,
    }

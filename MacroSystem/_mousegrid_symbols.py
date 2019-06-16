# coding: utf-8
# This grammar provides the symbols that can be spoken while the mouse grid is shown. It includes all keyboard
# characters but also many unicode symbols that aren't available on keyboards and therefore don't have keycodes,
# to allow fine-grained control of mouse grids while using only 1 or 2 characters on the screen. Since the whole
# purpose of this is to control the mouse grids, this module will just send that info to the mouse grid XMLRPC
# server directly instead of via keyboard events.
# By Shervin Emami (www.shervinemami.info), 2019.


from aenea import Grammar, MappingRule, Text, Key, Function, Choice, CompoundRule, ProxyAppContext
from collections import OrderedDict     # Allows ordered dictionaries even in Python 2

# Allow calling aenea server-side plugins
try:
    import aenea.communications
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise

# Allow passing any keypresses to the mouse grid window, since it's a root window that can't receive keypresses.
# We send them as direct input instead of as keycodes, since many of these symbols don't have corresponding key codes.
import xmlrpclib


from mousegridutils import loadAllSymbols
from mousegridutils import mouseActions


class SymbolEvent:
    def __init__(self, phrase, symbol):
        self.phrase = phrase
        self.symbol = symbol


# Set the IP address & port of the mouse grid XMLRPC server
MOUSE_SERVER_ADDRESS = 'http://192.168.56.1:8000'
server = xmlrpclib.ServerProxy(MOUSE_SERVER_ADDRESS)


# Create an ordered dictionary of all the symbols and phrases we might use in our mouse grids.
# Symbols that are easier to use should be placed near the top of the list, since some screens won't need to show the symbols on the bottom of the list.
# Rather than listen for all possible symbols in all cases, only listen for the actual symbols that can fit on the screen.
# Make sure you update "TOTAL_SYMBOLS_FOR_MINI_GRID" depending on your screen resolution and font size settings in "standalone_grids.py"!
TOTAL_SYMBOLS_FOR_2DGRID_X = 88
TOTAL_SYMBOLS_FOR_2DGRID_Y = 61
charsDict2D_X = loadAllSymbols(keyboardMode=False, extendedSymbolsLevel=3, extendedSymbolsCount=TOTAL_SYMBOLS_FOR_2DGRID_X)
charsDict2D_Y = loadAllSymbols(keyboardMode=False, extendedSymbolsLevel=3, extendedSymbolsCount=TOTAL_SYMBOLS_FOR_2DGRID_Y)
charsDict1D_X = loadAllSymbols(keyboardMode=False, extendedSymbolsLevel=3, extendedSymbolsCount=999999)
# charsDict1D_Y = charsDict2D_X   # 1D Y grid uses slightly less symbols than 2D X axis, so just re-use it
#print "charsDict2D_X", charsDict2D_X
#print "charsDict1D_X", charsDict1D_X


# Handle the various grid mode grammars
def doRecognitionLevel(node, extras, mode):
    # Get the input data
    symbol1 = ""
    symbol2 = ""
    mouseAction = -1
    try:
        symbol1 = extras["symbol1"]
    except:
        pass
    
    try:
        symbol2 = extras["symbol2"]
    except:
        pass
    
    try:
        mouseAction = extras["mouseAction"]
    except:
        pass

    #print node.pretty_string()
    words = node.words()
    print u"In doRecognitionLevel(), mode", mode, ". spoken words:", words,
    if len(symbol1) > 0:
        print symbol1.encode('utf-8'),
    if len(symbol2) > 0:
        print symbol2.encode('utf-8'),
    print u", mouse action", mouseAction

    # Move the mouse cursor by sending the symbol to the mouse grid RPC server.
    phrase1 = ""
    symbol1Event = None
    symbol2Event = None
    if len(symbol1) > 0:
        phrase1 = node.results[0][0] #.encode("utf-8")
        symbol1Event = SymbolEvent(phrase1, symbol1)
    phrase2 = ""
    if len(symbol2) > 0:
        phrase2 = node.results[1][0]
        symbol2Event = SymbolEvent(phrase2, symbol2)
    # If we have a symbol or possibly 2, send the 1 or 2 signals
    if symbol1Event:
        if symbol2Event:
            server.injectSymbols(symbol1Event, symbol2Event)
        else:
            server.injectSymbol(symbol1Event)

    # Possibly press a mouse button action
    button_int = int(mouseAction)
    if button_int >= 0:
        print "Calling clickMouseGrid(%d) on the server" % (button_int)
        # Run our aenea plugin script that moves and clicks the mouse in Linux.
        pid = aenea.communications.server.clickMouseGrid(button_int)


class MouseActionGridRule(CompoundRule):
    spec = "<mouseAction>"
    extras = [
        Choice("mouseAction", mouseActions),
    ]

    def _process_recognition(self, node, extras):
        doRecognitionLevel(node, extras, "Action")


class ExtraSymbolsMiniGridRule(CompoundRule):
    spec = "<symbol1> [<symbol2>] [<mouseAction>]"
    extras = [
        Choice("symbol1", charsDict2D_X),
        Choice("symbol2", charsDict2D_Y),
        Choice("mouseAction", mouseActions),
    ]

    def _process_recognition(self, node, extras):
        print u"node", node
        print u"extras", extras
        doRecognitionLevel(node, extras, "Mini")


class ExtraSymbolsFullGridRule(CompoundRule):
    spec = "<symbol1> [<mouseAction>]"
    extras = [
        Choice("symbol1", charsDict1D_X),
        Choice("mouseAction", mouseActions),
    ]

    def _process_recognition(self, node, extras):
        doRecognitionLevel(node, extras, "Full")


# Allow to easily close the mouse grid while it's displayed
def cancelMouseGrid():
    #print "Calling showMouseGrid(cancel) on the server to hide the MouseGrid"
    # Run our aenea plugin script that shows the mouse grid fullscreen in Linux.
    #aenea.communications.server.showMouseGrid("cancel")

    print "Sending Escape to cancel the mouse grid"
    action = Key("escape")
    action.execute()


class MouseCancelRule(MappingRule):
    mapping = {
        "cancel":    Function(cancelMouseGrid),
    }


contextMini = ProxyAppContext(title="InvisibleWindow - Mini")
grammarMini = Grammar('extra symbols mini grammar', context=contextMini)
grammarMini.add_rule(ExtraSymbolsMiniGridRule())
grammarMini.add_rule(MouseCancelRule())
grammarMini.add_rule(MouseActionGridRule())
grammarMini.load()

contextFull = ProxyAppContext(title="InvisibleWindow - Full")
grammarFull = Grammar('extra symbols full grammar', context=contextFull)
grammarFull.add_rule(ExtraSymbolsFullGridRule())
grammarFull.add_rule(MouseCancelRule())
grammarFull.add_rule(MouseActionGridRule())
grammarFull.load()


def unload():
    global grammarMini
    if grammarMini:
        grammarMini.unload()
    grammarMini = None

    global grammarFull
    if grammarFull:
        grammarFull.unload()
    grammarFull = None

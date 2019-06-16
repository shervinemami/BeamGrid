# coding: utf-8
# Keyboard & mouse macro recording & playback system and history playback system, for Dragonfly and/or Aenea.
# By Shervin Emami (www.shervinemami.info), 2019.


import dragonfly
from aenea import Grammar, MappingRule, CompoundRule, Text, Key, Mouse, Function, Playback, Choice, Dictation, ProxyAppContext, IntegerRef
#import json
import time
from collections import OrderedDict     # Allows ordered dictionaries even in Python 2

import xmlrpclib
from mousegridutils import smallNumbers


try:
    import aenea.communications
    #import aenea.config
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise


grammar = Grammar('aenea treasure macros grammar')

# An ordered dictionary, to allow incrementing numbers
historyNumber = OrderedDict()
historyNumber["one"] = u"one"
historyNumber["two"] = u"two"
historyNumber["three"] = u"three"
historyNumber["four"] = u"four"
historyNumber["five"] = u"five"
historyNumber["six"] = u"six"
historyNumber["seven"] = u"seven"
historyNumber["eight"] = u"eight"
historyNumber["nine"] = u"nine"
historyNumber["ten"] = u"ten"
historyNumber["eleven"] = u"eleven"
historyNumber["twelve"] = u"twelve"
historyNumber["thirteen"] = u"thirteen"
historyNumber["fourteen"] = u"fourteen"
historyNumber["fifteen"] = u"fifteen"


# Start recording all mouse & keyboard activity in the background, or playing a macro or history item.
def handleMacro(mode, label):
    retVal = aenea.communications.server.recordOrPlay(mode, label)

    # Check if the returned value was an integer (the PID) or a list of strings (the playback message).
    isList = isinstance(retVal, list)
    if isList:
        # We want Dragon to playback the command
        print u"Playing back", retVal, u"using Dragon."
        action = dragonfly.Playback([(retVal, 0.0)])
        action.execute()


# label and mode are required. label2 is optional
def controlRecordings(node, extras):
    label = extras["label"]
    mode = extras["mode"]

    # Only allow repetition of playback
    repetitions = 1
    try:
        repetitions = extras["repetitions"]
        if mode != "play":
            repetitions = 1
    except:
        pass

    label2 = ""
    label3 = ""
    try:
        label2 = extras["label2"]
        #label2 = unicode(label2)
        label3 = extras["label3"]
        #label3 = unicode(label3)
        print u"Found extra play commands", label2, u"and", label3
    except:
        pass

    # Convert the Dragonfly object into a string of words
    label = unicode(label)
    print u"Beginning to", mode, u"macro", label, u"for both keyboard & mouse,", repetitions, u"times."
    
    for i in range(repetitions):
        # Start recording all mouse & keyboard activity in the background, or playing a macro or history item.
        handleMacro(mode, label)
        
        # Play the other macros or history items, if given
        if len(label2) > 0:
            # Since playback of each item causes 2 more entries in the history, we need to add 2 to the history number
            numbersList = historyNumber.keys()
            c2 = -1
            c3 = -1
            try:
                c2 = numbersList.index(label2)
                c3 = numbersList.index(label3)
            except:
                print u"Couldn't find label2", label2, "or label3", label3
            if c2 >= 0:
                label2 = numbersList[c2 + 2]
                handleMacro(mode, label2)
            if c3 >= 0:
                label3 = numbersList[c3 + 3]
                handleMacro(mode, label3)

        time.sleep(0.01)


class ControlRecordingRule(CompoundRule):
    spec = "<mode> [<label>]"
    extras = [
        Choice("mode", {
                "record": "record",
                "delete recording": "delete",
                "show recordings": "show",
            }),
        Dictation(name='label'),
    ]
    defaults = {
        "label": "default",
    }
    
    def _process_recognition(self, node, extras):
        controlRecordings(node, extras)


class PlayRecordingRule(CompoundRule):
    spec = "<mode> [<label>] [<repetitions> times]"
    extras = [
        Choice("mode", {
                "play": "play",
            }),
        Dictation(name='label'),
        Choice("repetitions", smallNumbers),
    ]
    defaults = {
        "label": "default",
        "repetitions": 1,
    }
    
    def _process_recognition(self, node, extras):
        controlRecordings(node, extras)


class PlayHistoryRule(CompoundRule):
    spec = "<mode> <label> [and <label2> [and <label3>]] [<repetitions> times]"
    extras = [
        Choice("mode", {
                "play": "play",
            }),
        Choice("label", historyNumber),
        Choice("label2", historyNumber),
        Choice("label3", historyNumber),
        Choice("repetitions", smallNumbers),
    ]
    defaults = {
        "label": "",
        "label2": "",
        "label3": "",
        "repetitions": 1,
    }
    
    def _process_recognition(self, node, extras):
        controlRecordings(node, extras)


class StopRecordingRule(CompoundRule):
    spec = "stop recording"
    
    def _process_recognition(self, node, extras):
        print "Stopping macro recording."
        
        # Stop the recording program.
        pid = aenea.communications.server.recordOrPlay("stop", "")



grammar.add_rule(ControlRecordingRule())
grammar.add_rule(PlayRecordingRule())
grammar.add_rule(PlayHistoryRule())
grammar.add_rule(StopRecordingRule())
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

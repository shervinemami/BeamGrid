# This is a command module for Dragonfly. It provides support for several of
# Aenea's built-in capabilities. This module is NOT required for Aenea to
# work correctly, but it is strongly recommended.

# This file is part of Aenea
#
# Aenea is free software: you can redistribute it and/or modify it under
# the terms of version 3 of the GNU Lesser General Public License as
# published by the Free Software Foundation.
#
# Aenea is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Aenea.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (2014) Alex Roper
# Alex Roper <alex@aroper.net>

import os
import sys
import time

import dragonfly
from dragonfly.grammar.recobs import RecognitionObserver

try:
    # Internal NatLink module for reloading grammars.
    import natlinkmain
except ImportError:
    natlinkmain = None

try:
    import aenea
    import aenea.proxy_contexts
    import aenea.configuration
    import aenea.communications
    import aenea.config
    import aenea.configuration
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise

print 'Aenea client-side modules loaded successfully'
print 'Settings:'
print '\tHOST:', aenea.config.DEFAULT_SERVER_ADDRESS[0]
print '\tPORT:', aenea.config.DEFAULT_SERVER_ADDRESS[1]
print '\tPLATFORM:', aenea.config.PLATFORM
print '\tUSE_MULTIPLE_ACTIONS:', aenea.config.USE_MULTIPLE_ACTIONS
print '\tSCREEN_RESOLUTION:', aenea.config.SCREEN_RESOLUTION

try:
    aenea.proxy_contexts._get_context()
    print 'Aenea: Successfully connected to server.'
except:
    print 'Aenea: Unable to connect to server.'


# Try to load the OS functions if they exist, otherwise use empty functions.
def changeToLinux():
    pass
def changeToWindows():
    pass
def microphoneStateCallback(cbType, args):
    pass
def logRecognition(msg):
    pass
try:
    from systemutils import changeToLinux
    from systemutils import changeToWindows
    from systemutils import microphoneStateCallback
    from systemutils import logRecognition
except:
    pass


# Commands that can be rebound.
command_table = [
    'set proxy server to <proxy>',
    'disable proxy server',
    'enable proxy server',
    'force natlink to reload all grammars',
    'disable keyboard',
    'enable keyboard',
    'shervs test',
    'pause',
    'play music',
    'change to Linux',
    'change to Windows',
    'window list',
    'shelf list',
    'show history',     # Note that "Show Recognition History" is already a native command in Dragon
    ]
command_table = aenea.configuration.make_grammar_commands(
    'aenea',
    dict(zip(command_table, command_table))
    )


def topy(path):
    if path.endswith == ".pyc":
        return path[:-1]

    return path


#----------------------------------------------------------------------------------------------------------
# Send all Dragon recognitions to Linux using Aenea so it can be displayed on the host machine.
class LinuxRecognitionEcho(RecognitionObserver):
    """Handler that echoes the recognition in Linux"""

    #def __init__(self):
    #    self.wordsList = []

    def on_begin(self):
        logRecognition("...")

    def on_recognition(self, words):
        wordsString = ' '.join(words)
        logRecognition(wordsString)
        print "SPOKEN:", wordsString
        print

    def on_failure(self):
        logRecognition("<???>")
        print "SPOKEN: <???>"
        print

linux_echo_handler = LinuxRecognitionEcho()

# Register our recognition observer with Dragon. Note that we will also unregister it when grammars are unloaded,
# otherwise there will be multiple echo handlers running at the same time!
linux_echo_handler.register()


#----------------------------------------------------------------------------------------------------------
# Natlink callback function for whenever the Dragon microphone changes state between awake and sleep!
def changeCallback(cbType, args):
    print cbType, # 'mic' or 'user'
    print "=",
    print args    # 'off', 'on', 'disabled' or 'sleeping'.
    if cbType == "mic":
        microphoneStateCallback(cbType, args)

#----------------------------------------------------------------------------------------------------------

class DisableRule(dragonfly.CompoundRule):
    spec = command_table['disable proxy server']

    def _process_recognition(self, node, extras):
        logRecognition("disable proxy server")
        aenea.config.disable_proxy()


class EnableRule(dragonfly.CompoundRule):
    spec = command_table['enable proxy server']

    def _process_recognition(self, node, extras):
        logRecognition("enable proxy server")
        aenea.config.enable_proxy()


def unload_code(optional_blacklist = []):
    print "Unloading all aenea code"

    # Do not reload anything in these directories or their subdirectories.
    #blacklist_list = list("core") + optional_blacklist
    dir_reload_blacklist = set(["core"])
    if len(optional_blacklist):
        dir_reload_blacklist.add(optional_blacklist)
    print "Blacklist: ", dir_reload_blacklist
    macro_dir = "C:\\NatLink\\NatLink\\MacroSystem"

    # Unload all grammars if natlinkmain is available.
    if natlinkmain and not len(optional_blacklist):
        natlinkmain.unloadEverything()

    # Unload all modules in macro_dir except for those in directories on the
    # blacklist.
    # Consider them in sorted order to try to make things as predictable as possible to ease debugging.
    for name, module in sorted(sys.modules.items()):
        if module and hasattr(module, "__file__"):
            # Some builtin modules only have a name so module is None or
            # do not have a __file__ attribute.  We skip these.
            path = module.__file__

            # Convert .pyc paths to .py paths.
            path = topy(path)

            # Do not unimport this module!  This will cause major problems!
            if (path.startswith(macro_dir) and
                not bool(set(path.split(os.path.sep)) & dir_reload_blacklist)
                and path != topy(os.path.abspath(__file__))):

                print "removing %s from cache (in module %s)" % (name, module)

                # Remove the module from the cache so that it will be reloaded
                # the next time # that it is imported.  The paths for packages
                # end with __init__.pyc so this # takes care of them as well.
                del sys.modules[name]

def load_code():
    print "Loading all aenea code"
    try:
        # Reload the top-level modules in macro_dir if natlinkmain is available.
        if natlinkmain:
            natlinkmain.findAndLoadFiles()
    except Exception as e:
        print "reloading failed: {}".format(e)
    else:
        print "finished reloading"

def reload_code():
    logRecognition("force natlink to reload all grammars")
    unload_code()
    load_code()


def disableKeyboard():
    print "Disabling just the keyboard grammar."
    logRecognition("disable keyboard")
    # Unload the modules except for all the "core" and "aenea" modules
    unload_code("aenea")

    print "Switching Dragon to Normal mode."
    action = dragonfly.Mimic("switch", "to", "normal", "mode")
    #action = dragonfly.Playback([(["switch", "to", "normal", "mode"], 0.0)])
    action.execute()


def enableKeyboard():
    print "Enabling keyboard."
    logRecognition("enable keyboard")
    load_code()

    print "Switching Dragon to Command mode."
    action = dragonfly.Mimic("switch", "to", "command", "mode")
    #action = dragonfly.Playback([(["switch", "to", "command", "mode"], 0.0)])
    action.execute()


def shervstest():
    print "Running Shervs Test!"
    logRecognition("shervs test")
    
    #from six.moves import xmlrpc_client
    #server = xmlrpc_client.ServerProxy("http://127.0.0.1:12400", allow_none=False)
    #remote_title = server.GetActiveWindowTitle()
    #print "Remote ", remote_title


def pauseDragon():
    print "Pausing Dragon"
    logRecognition("pause")
    # Pause Dragon, similar to saying "Stop Listening"
    action = dragonfly.Key("npdiv")     # Numpad "/" key
    action.execute()
    
    # Also pause my music player
    #action = aenea.Key("ctrl:down, shift:down, f12") + aenea.Key("ctrl:up, shift:up")
    #action.execute()
    pid = aenea.communications.server.controlMusic("pause")


def playMusic():
    print "Playing music"
    #logRecognition("play music")
    # Play my music player
    #action = aenea.Key("ctrl:down, shift:down, f12") + aenea.Key("ctrl:up, shift:up")
    #action.execute()
    pid = aenea.communications.server.controlMusic("play")


def showWindowList():
    print "Showing the Linux window list."
    logRecognition("window list")

    #"show window list":      Key("win:down/999, tab") + Key("win:up"),
    #"show window list":      Key("w-l") + Key("tab") + Key("down"),
    #action = aenea.Key("ctrl:down, alt:down") + aenea.Key("ctrl:up, alt:up")
    #action = aenea.Key("ctrl:down") + aenea.Key("o")
    #action.execute()
    #time.sleep(0.3)
    #action = aenea.Key("tab")
    #action.execute()
    #time.sleep(0.1)
    #action = aenea.Key("down")
    #action.execute()

    # Run our aenea plugin script that shows the Linux window list.
    aenea.communications.server.showWindowList()


def showHistory():
    print "Showing the recognition history."

    # Run our aenea plugin script that shows the Dragon recognition history
    aenea.communications.server.showHistory()


def showShelfList():
    print "Showing the Linux shelf list."
    logRecognition("shelf list")

    # Run our aenea plugin script that shows the Linux clipboard shelf list.
    # Value -1 means show the graphical list.
    aenea.communications.server.shelfCommand(-1)

def shelfNumber(val):
    print "Running shelf number", val
    logRecognition("shelf " + val)

    # Run our aenea plugin script that pastes the shelf item
    aenea.communications.server.shelfCommand(val)


class DisableKeyboard(dragonfly.MappingRule):
    mapping = {command_table['disable keyboard']: dragonfly.Function(disableKeyboard)}

class EnableKeyboard(dragonfly.MappingRule):
    mapping = {command_table['enable keyboard']: dragonfly.Function(enableKeyboard)}

class ShervsTest(dragonfly.MappingRule):
    mapping = {command_table['shervs test']: dragonfly.Function(shervstest)}

class PauseDragon(dragonfly.MappingRule):
    mapping = {command_table['pause']: dragonfly.Function(pauseDragon)}

class PlayMusic(dragonfly.MappingRule):
    mapping = {command_table['play music']: dragonfly.Function(playMusic)}

class ChangeToLinux(dragonfly.MappingRule):
    mapping = {command_table['change to Linux']: dragonfly.Function(changeToLinux)}

class ChangeToWindows(dragonfly.MappingRule):
    mapping = {command_table['change to Windows']: dragonfly.Function(changeToWindows)}

class ShowWindowList(dragonfly.MappingRule):
    mapping = {command_table['window list']: dragonfly.Function(showWindowList)}

class ShowShelfList(dragonfly.MappingRule):
    mapping = {command_table['shelf list']: dragonfly.Function(showShelfList)}

class ShowHistory(dragonfly.MappingRule):
    mapping = {command_table['show history']: dragonfly.Function(showHistory)}

class ShelfNumber(dragonfly.MappingRule):
    mapping = {
        # Call shelfNumber(<n>)
        "shelf <n>": dragonfly.Function(lambda n: shelfNumber(n))
    }
    extras = [
        dragonfly.IntegerRef("n", 0, 99),
    ]
    #defaults = {
    #    "n": 0,
    #}

# Note that you do not need to turn mic off and then on after saying this.  This
# also unloads all modules and packages in the macro directory so that they will
# be reloaded the next time that they are imported.  It even reloads Aenea!
class ReloadGrammarsRule(dragonfly.MappingRule):
    mapping = {command_table['force natlink to reload all grammars']: dragonfly.Function(reload_code)}

server_list = dragonfly.DictList('aenea servers')
server_list_watcher = aenea.configuration.ConfigWatcher(
    ('grammar_config', 'aenea'))


class ChangeServer(dragonfly.CompoundRule):
    spec = command_table['set proxy server to <proxy>']
    extras = [dragonfly.DictListRef('proxy', server_list)]

    def _process_recognition(self, node, extras):
        aenea.communications.set_server_address((extras['proxy']['host'], extras['proxy']['port']))

    def _process_begin(self):
        if server_list_watcher.refresh():
            server_list.clear()
            for k, v in server_list_watcher.conf.get('servers', {}).iteritems():
                server_list[str(k)] = v

grammar = dragonfly.Grammar('aenea')

grammar.add_rule(EnableRule())
grammar.add_rule(DisableRule())
grammar.add_rule(ReloadGrammarsRule())
grammar.add_rule(ChangeServer())
grammar.add_rule(DisableKeyboard())
grammar.add_rule(EnableKeyboard())
grammar.add_rule(ShervsTest())
grammar.add_rule(PauseDragon())
grammar.add_rule(PlayMusic())
grammar.add_rule(ChangeToLinux())
grammar.add_rule(ChangeToWindows())
grammar.add_rule(ShowWindowList())
grammar.add_rule(ShowShelfList())
grammar.add_rule(ShowHistory())
grammar.add_rule(ShelfNumber())

grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
    
    global linux_echo_handler
    linux_echo_handler.unregister()

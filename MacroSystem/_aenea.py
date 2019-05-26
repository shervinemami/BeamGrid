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


# Commands that can be rebound.
command_table = [
    'set proxy server to <proxy>',
    'disable proxy server',
    'enable proxy server',
    'force natlink to reload all grammars',
    'disable keyboard',
    'enable keyboard',
    'shervs test',
    'change to Linux',
    'change to Windows',
    'window list',
    'shelf list',
    ]
command_table = aenea.configuration.make_grammar_commands(
    'aenea',
    dict(zip(command_table, command_table))
    )


def topy(path):
    if path.endswith == ".pyc":
        return path[:-1]

    return path


class DisableRule(dragonfly.CompoundRule):
    spec = command_table['disable proxy server']

    def _process_recognition(self, node, extras):
        aenea.config.disable_proxy()


class EnableRule(dragonfly.CompoundRule):
    spec = command_table['enable proxy server']

    def _process_recognition(self, node, extras):
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
    unload_code()
    load_code()


def disableKeyboard():
    print "Disabling just the keyboard grammar."
    # Unload the modules except for all the "core" and "aenea" modules
    unload_code("aenea")

    print "Switching Dragon to Normal mode."
    action = dragonfly.Mimic("switch", "to", "normal", "mode")
    #action = dragonfly.Playback([(["switch", "to", "normal", "mode"], 0.0)])
    action.execute()


def enableKeyboard():
    print "Enabling keyboard."
    load_code()

    print "Switching Dragon to Command mode."
    action = dragonfly.Mimic("switch", "to", "command", "mode")
    #action = dragonfly.Playback([(["switch", "to", "command", "mode"], 0.0)])
    action.execute()


def shervstest():
    print "Running Shervs Test!"

    #from six.moves import xmlrpc_client
    #server = xmlrpc_client.ServerProxy("http://127.0.0.1:12400", allow_none=False)
    #remote_title = server.GetActiveWindowTitle()
    #print "Remote ", remote_title


# Switching OSes, when Windows is in a VM on top of a Linux host:
def changeToLinuxVM():
    print "Changing to Linux from Windows VM!"

    # Run our aenea plugin script that moves the Windows VM to a minimally visible window in Linux.
    print "Calling change OS"
    aenea.communications.server.change_OS("Linux")
    print "Finished calling change OS"
    time.sleep(0.1)

    print "Switching Dragon to Command mode."
    action = dragonfly.Mimic("switch", "to", "command", "mode")
    #action = dragonfly.Playback([(["switch", "to", "command", "mode"], 0.0)])
    action.execute()
    time.sleep(0.1)

    # Make sure all keyboard input gets relayed to the Linux aenea server!
    #action = dragonfly.Mimic("switch", "to", "Aenea", "client")
    #action = dragonfly.Playback([(["switch", "to", "Aenea", "client"], 0.0)])
    #action = dragonfly.FocusWindow(title="Aenea client")
    #action.execute()
    #time.sleep(0.3)

    # Move the keyboard focus in Windows to a text box, so I can't accidentally type messages in Windows while I'm looking at Linux!
    # The Windows keyboard focus can be controlled even while I'm in Linux, so we do it after the importance of have already happened above.
    #action = dragonfly.Mimic("switch", "to", "notepad")
    #action = dragonfly.FocusWindow(title="Notepad")
    #action = dragonfly.Mimic("control", "one")
    #action = dragonfly.Mimic("control", "foxy")  # Open the Firefox search bar, so I can still read chats but not type into them
    #action = dragonfly.Mimic("control", "lazy")  # Focus on the location bar
    #action.execute()
    #time.sleep(0.3)


# Switching OSes, when Windows is in a VM on top of a Linux host:
def changeToWindowsVM():
    print "Changing to Windows VM from Linux!"

    # Run our aenea plugin script that moves the Windows VM to fullscreen in Linux.
    aenea.communications.server.change_OS("Windows")
    time.sleep(0.3)

    # Make sure the keyboard input doesn't go to the Linux aenea server!
    #action = dragonfly.Mimic("start", "dragonpad")
    #action = dragonfly.BringApp("")
    #action = dragonfly.Playback([(["alt", "escape"], 0.0)])
    #action = dragonfly.Key("alt") + dragonfly.Key("escape")
    #action = dragonfly.FocusWindow(title="Firefox")
    # Change the Windows browser to the Slack tab
    # The Windows keyboard focus can be controlled even while I'm in Linux, so we do it after the importance of have already happened above.
    #action = dragonfly.Mimic("control", "four")
    #action = dragonfly.Mimic("F6")
    #action.execute()
    #time.sleep(0.6)

    print "Switching Dragon to Normal mode."
    action = dragonfly.Mimic("switch", "to", "normal", "mode")
    #action = dragonfly.Playback([(["switch", "to", "normal", "mode"], 0.0)])
    action.execute()
    time.sleep(0.3)

    # Make sure the DragonPad menu bar isn't selected
    #action = dragonfly.Mimic("escape")
    #action.execute()
    time.sleep(0.3)


# Switching OSes, when Windows is another PC:
def changeToWindowsNative():
    print "Changing to native Windows PC from other Linux PC!"
    action = dragonfly.Mimic("gravy")
    action.execute()
    time.sleep(0.2)
    action = dragonfly.Mimic("switch", "to", "normal", "mode")
    action.execute()
    time.sleep(0.2)
    aenea.config.disable_proxy()
    time.sleep(0.3)

# Switching OSes, when Windows is another PC:
def changeToLinuxNative():
    print "Changing to Linux PC from other native Windows PC!"
    action = dragonfly.Mimic("switch", "to", "command", "mode")
    action.execute()
    time.sleep(0.2)
    aenea.config.enable_proxy()
    time.sleep(0.3)
    action = dragonfly.Mimic("porridge")
    action.execute()


def changeToWindows():
    #changeToWindowsNative()
    changeToWindowsVM()

def changeToLinux():
    #changeToLinuxNative()
    changeToLinuxVM()


def showWindowList():
    print "Showing the Linux window list."

    #"show window list":      Key("win:down/999, tab") + Key("win:up"),
    #"show window list":      Key("w-l") + Key("tab") + Key("down"),
    #action = dragonfly.Key("ctrl:down, alt:down") + dragonfly.Key("ctrl:up, alt:up")
    #action = dragonfly.Key("ctrl:down") + dragonfly.Key("o")
    #action.execute()
    #time.sleep(0.3)
    #action = dragonfly.Key("tab")
    #action.execute()
    #time.sleep(0.1)
    #action = dragonfly.Key("down")
    #action.execute()

    # Run our aenea plugin script that shows the Linux window list.
    aenea.communications.server.showWindowList()


def showShelfList():
    print "Showing the Linux shelf list."

    # Run our aenea plugin script that shows the Linux clipboard shelf list.
    # Value -1 means show the graphical list.
    aenea.communications.server.shelfCommand(-1)

def shelfNumber(val):
    print "Running shelf number", val

    # Run our aenea plugin script that pastes the shelf item
    aenea.communications.server.shelfCommand(val)


class DisableKeyboard(dragonfly.MappingRule):
    mapping = {command_table['disable keyboard']: dragonfly.Function(disableKeyboard)}

class EnableKeyboard(dragonfly.MappingRule):
    mapping = {command_table['enable keyboard']: dragonfly.Function(enableKeyboard)}

class ShervsTest(dragonfly.MappingRule):
    mapping = {command_table['shervs test']: dragonfly.Function(shervstest)}

class ChangeToLinux(dragonfly.MappingRule):
    mapping = {command_table['change to Linux']: dragonfly.Function(changeToLinux)}

class ChangeToWindows(dragonfly.MappingRule):
    mapping = {command_table['change to Windows']: dragonfly.Function(changeToWindows)}

class ShowWindowList(dragonfly.MappingRule):
    mapping = {command_table['window list']: dragonfly.Function(showWindowList)}

class ShowShelfList(dragonfly.MappingRule):
    mapping = {command_table['shelf list']: dragonfly.Function(showShelfList)}

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
grammar.add_rule(ChangeToLinux())
grammar.add_rule(ChangeToWindows())
grammar.add_rule(ShowWindowList())
grammar.add_rule(ShowShelfList())
grammar.add_rule(ShelfNumber())

grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

# coding: utf-8
# Use mouse grids to control the mouse by voice on a possibly remote machine and different OS, through Aenea.
# Based on Caster's DouglasGrid
# By Shervin Emami (www.shervinemami.info), 2019.


from aenea import Grammar, MappingRule, CompoundRule, Text, Key, Mouse, Function, Playback, Choice, ProxyAppContext, IntegerRef
#import json

import xmlrpclib

MOUSE_SERVER_ADDRESS =           'http://192.168.56.1:8000'
INVISIBLEWINDOW_SERVER_ADDRESS = 'http://192.168.56.1:8001'

mouseServer = xmlrpclib.ServerProxy(MOUSE_SERVER_ADDRESS)
windowServer = xmlrpclib.ServerProxy(INVISIBLEWINDOW_SERVER_ADDRESS)

try:
    import aenea.communications
    #import aenea.config
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise

from mousegridutils import mouseActions
from mousegridutils import mostNumbers


grammar = Grammar('aenea mouse start grammar')


class CenterMouseRule(CompoundRule):
    spec = "center [<mouseAction>]"
    extras = [
        Choice("mouseAction", mouseActions),
    ]
    defaults = {
        # Set the default to -1 if you want "center" to just move the cursor,
        # or set it to 1 if you want "center" to perform a left mouse click by default.
        "mouseAction": 1,
    }

    def _process_recognition(self, node, extras):
        mouseAction = extras["mouseAction"]
        
        print "Centering the mouse."
        try:
            mouseServer.moveToCenter()
        except:
            print "Couldn't access the mouse grid server, is it running?"
            return
        
        # Possibly press a mouse button action
        button_int = int(mouseAction)
        if button_int >= 0:
            print "Calling clickMouseGrid(%d) on the server" % (button_int)
            # Run our aenea plugin script that moves and clicks the mouse in Linux.
            pid = aenea.communications.server.clickMouseGrid(button_int)


class NudgeMouseRule(CompoundRule):
    spec = "nudge <direction> [<distance>] [<mouseAction>]"
    extras = [
        Choice("mouseAction", mouseActions),
        Choice("direction", {                       # Allow to say either up or North
            "North":        1,
            "East":         2,
            "South":        3,
            "West":         4,
            "North East":   5,
            "South East":   6,
            "South West":   7,
            "North West":   8,
            "up":         1,
            "right":      2,
            "down":       3,
            "left":       4,
            "up right":   5,
            "down right": 6,
            "down left":  7,
            "up left":    8,
            }),
        Choice("distance", mostNumbers),
    ]
    defaults = {
        "mouseAction": -1,  # Don't click unless they ask for it
    }
    
    def _process_recognition(self, node, extras):
        direction = extras["direction"]
        mouseAction = extras["mouseAction"]
        
        # Figure out how much to move by
        distance = 7  # Default distance to nudge by
        try:
            distance = extras["distance"]
        except:
            pass
        
        print "Nudging the mouse in direction", direction, "by", distance
        try:
            if direction == 1:
                mouseServer.move_mouse_relative(0, -distance)
            elif direction == 2:
                mouseServer.move_mouse_relative(distance, 0)
            elif direction == 3:
                mouseServer.move_mouse_relative(0, distance)
            elif direction == 4:
                mouseServer.move_mouse_relative(-distance, 0)
            elif direction == 5:
                mouseServer.move_mouse_relative(distance, -distance)
            elif direction == 6:
                mouseServer.move_mouse_relative(distance, distance)
            elif direction == 7:
                mouseServer.move_mouse_relative(-distance, distance)
            elif direction == 8:
                mouseServer.move_mouse_relative(-distance, -distance)
        except:
            print "Couldn't access the mouse grid server, is it running?"
            return
        
        # Possibly press a mouse button action
        button_int = int(mouseAction)
        if button_int >= 0:
            print "Calling clickMouseGrid(%d) on the server" % (button_int)
            # Run our aenea plugin script that moves and clicks the mouse in Linux.
            pid = aenea.communications.server.clickMouseGrid(button_int)


def showMouseGrid(mode, mouseClick=-1):
    print "Calling showMouseGrid(%s) on the server" % (mode)

    # We need to specify whether the mouse mode we are controlling in later commands.
    #aenea.mouse_grid_mode = "x"

    # Run our aenea plugin script that shows the mouse grid fullscreen in Linux.
    #pid = aenea.communications.server.showMouseGrid("x0")

    # Display the mouse grid
    try:
        mouseServer.showMouseGrid(mode, mouseClick)
    except:
        print "Couldn't access the mouse grid server, is it running?"
        return

    # Make sure the invisible window is brought to the front of the window stack, so it can have keyboard focus to be used with our extra characters.
    print "Showing the InvisibleWindow"
    try:
        windowServer.unhide()
    except:
        print "Couldn't access the InvisibleWindow server, is it running?"
        return

    print "Finished showMouseGrid(%s)" % (mode)


def showMouseGridX0():
    showMouseGrid("x0")

def showMouseGridX1():
    showMouseGrid("x1")

def showMouseGridX2():
    showMouseGrid("x2")

def showMouseGridY0():
    showMouseGrid("y0")

# Show a sequence of 2 grids moving in a single direction at a time
def showMouseGridX0Y0():
    showMouseGrid("x0y0")

def clickMouseGridG0():
    # Show the mouse grid, but also schedule a left-mouse click when the user has finally moved the mouse pointer,
    # to save the user from needing a separate command to perform the mouse click.
    showMouseGrid("g0", mouseClick=1)

def showMouseGridG0():
    showMouseGrid("g0")

    #print "Calling showMouseGrid(2D) on the server"
    # We need to specify whether which mouse mode we are controlling in later commands.
    #aenea.mouse_grid_mode = "2D"

    # Run our aenea plugin script that shows the mouse grid fullscreen in Linux.
    #pid = aenea.communications.server.showMouseGrid("2D")
    #print "Returned pid", pid

    ## Reset the stored mouse status.
    #mouseState = {}
    #mouseState['x'] = -1
    #mouseState['y'] = -1
    #mouseState['status'] = 0    # Empty
    #
    ## Store the mouse status.
    #dir = ""
    #if len(aenea.config.PROJECT_ROOT) > 0:
    #    dir = aenea.config.PROJECT_ROOT + "\\"
    #with open(dir + "mouse_state.json", 'wb') as outfile:
    #    json.dump(mouseState, outfile)

    # We need to specify which mouse mode we are controlling in later commands.
    #aenea.mouse_grid_mode = "y"

    # Run our aenea plugin script that shows the mouse grid fullscreen in Linux.
    #pid = aenea.communications.server.showMouseGrid("y")
    #print "Returned pid", pid


class StartMouseGridRule(MappingRule):
    mapping = {
        # Commands for starting the mouse grid. The grid might only cover part of a large screen,
        # or you might have multiple screens, so we have commands to show grids in multiple locations.
        "sink":     Function(showMouseGridY0),      # Slide down or up
        "glide":    Function(showMouseGridX0),      # Slide left or right
        "sled":     Function(showMouseGridX0),      # Slide to the left screen
        "sliddle":  Function(showMouseGridX1),      # Slide to the inner screen
        "slight":   Function(showMouseGridX2),      # Slide to the right screen
        "grid":     Function(showMouseGridG0),      # 2D grid
        "beam":     Function(clickMouseGridG0),     # 2D grid + left mouse click
        "ladder":   Function(showMouseGridX0Y0),    # Show a sequence of 2 grids moving in a single direction
    }


grammar.add_rule(StartMouseGridRule())
grammar.add_rule(CenterMouseRule())
grammar.add_rule(NudgeMouseRule())

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

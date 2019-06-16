# coding: utf-8
# Modified version of Caster's grids.py, to include a "BeamGrid" mode for Aenea on Linux.
# Modified by Shervin Emami (www.shervinemami.info), 2019.

from __future__ import division

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib

import getopt
import signal
import sys
import os
from threading import Timer
import time
#import curses
from datetime import datetime
import subprocess
from collections import OrderedDict     # Allows ordered dictionaries even in Python 2
import operator

#import win32api

# These 2 lines are different for Python 2 vs 3
import Tkinter as tk
import tkFont as tkfont

from pynput.mouse import Button, Controller
mouse = Controller()

# Import the "letterMap" and similar dictionaries from the "lettermap.py" and similar files that are in the MacroSystem folder.
# Make sure you adjust this path to where it's located on your machine, relative to this script.
sys.path.append('../../../my_dragonfly_grammar/MacroSystem')
from mousegridutils import loadAllSymbols


# Set the IP address & port of the mouse grid XMLRPC server and the invisible window XMLRPC server
MOUSE_SERVER_ADDRESS = ("192.168.56.1", 8000)                # Set up our server address
INVISIBLEWINDOW_SERVER_ADDRESS = 'http://192.168.56.1:8001'  # Set up our client address
windowServer = xmlrpclib.ServerProxy(INVISIBLEWINDOW_SERVER_ADDRESS)

# Set the desired font of the 1D grids. It's very beneficial if this can be the same size as the font you use in your main apps & IDEs,
# so you can select every single character on your screen or in your IDE or console terminal.
fontFamily = "DejaVu Sans Mono"  #"Liberation Mono"
fontSize = 10
fontWeight = "normal"

# For the 1D grids, set these to the fixed character size of your chosen font.
charWidth = 10
charHeight = 15


TRANSPARENCY_LEVEL = 0.8

# If there aren't enough characters to cover your whole screen, it can use different colored grids of text
textColors = ['Blue', 'Green', 'Red', 'Dark Violet', 'Brown4', 'Black']
textNames = ['Blue', 'Green', 'Red', 'Purple', 'Brown', 'Black']


#from dragonfly import monitors

#try:  # Style C -- may be imported into Caster, or externally
#    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "caster", 1)[0]
#    if BASE_PATH not in sys.path:
#        sys.path.append(BASE_PATH)
#finally:
#    from caster.lib import settings, utilities
#    from caster.lib.dfplus.communication import Communicator

#try:
#    from PIL import ImageGrab, ImageTk, ImageDraw, ImageFont
#except ImportError:
#    print("Douglas Grid / Rainbow Grid / Beam Grid", "PIL")


#def wait_for_death(title, timeout=5):
#    t = 0.0
#    inc = 0.1
#    while t < timeout:
#        if not utilities.window_exists(None, title):
#            break
#        t += inc
#        time.sleep(inc)
#    if t >= timeout:
#        print("wait_for_death()" + " timed out (" + title + ")")


class KeyEvent:
    def __init__(self, char, keysym, keycode):
        self.char = char
        self.keysym = keysym
        self.keycode = keycode

class MouseButtonEvent:
    def __init__(self, x_root, y_root, button):
        self.x_root = x_root
        self.y_root = y_root
        self.button = button

# Allow receiving input as direct RPC data instead of as keycodes, since many extra symbols don't have corresponding key codes.
class SymbolEvent:
    def __init__(self, phrase, symbol):
        self.phrase = phrase
        self.symbol = symbol

class Dimensions:
    def __init__(self, w, h, x, y):
        self.width = w
        self.height = h
        self.x = x
        self.y = y

# Restrict XMLRPC server to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# rewrite dp grid using this
class TkTransparent(tk.Tk):
    def reset_xs_ys(self):
        self.xs = []
        self.ys = []

    def xs_ys_filled(self):
        return len(self.xs) > 0 or len(self.ys) > 0

    def get_dimensions_fullscreen(self):
        return Dimensions(self.winfo_screenwidth(), self.winfo_screenheight(), 0, 0)

    def get_dimensions_string(self):
        return "%dx%d+%d+%d" % (self.dimensions.width, self.dimensions.height,
                                self.dimensions.x, self.dimensions.y)

    def __init__(self, name, dimensions=None, canvas=True, axis='Ignored', serviceMode=False, keyboardMode=False):
        tk.Tk.__init__(self, baseName="TkTransparent")
        self.setup_xmlrpc_server()
        if not dimensions:
            dimensions = self.get_dimensions_fullscreen()
        self.wm_geometry("1x1+0+0")     # Start by showing a tiny pixel sized window that isn't obvious
        self.dimensions = dimensions

        # Load all symbols including the hard ones.
        print
        self.charsDict = loadAllSymbols(keyboardMode, 100000)

        self.reset_xs_ys()
        self.overrideredirect(True)     # Disable window borders, but also hide from the window manager
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.title(name)
        self.wm_title(name)
        #self.client(name)
        self.transient()                # Give further hint that this window shouldn't be shown in the Windows taskbar
        self.wait_visibility(self)
        self.attributes("-alpha", TRANSPARENCY_LEVEL)  # Show this whole window as semi-transparent. This line must be after "wait_visibility".
        self.wm_geometry(self.get_dimensions_string())  # Make this window fullscreen.
        self.mouseGridMode = ""
        self.highlightColumn = -1
        self.timerMidway = None
        self.queueMouseClick = -1
        self.keyboardMode = keyboardMode

        # Generate the unicode charString that can be rendered easily.
        self.charsString = u""
        for v in self.charsDict.values():
            self.charsString = self.charsString + v
        #print u"String of characters:", self.charsString

        if canvas:
            self._canvas = tk.Canvas(
                master=self,
                width=dimensions.width,
                height=dimensions.height,
                bg='white',
                bd=-2)
            #self._canvas.pack()
        self.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)

        # Close this window if any mouse or keyboard events happen. (Not expected conditions)
        self.bind("<Button-1>", self.mouseButton1_callback)
        self.bind("<Button-2>", self.mouseButton2_callback)
        self.bind("<Button-3>", self.mouseButton3_callback)
        self.bind("<KeyPress>", self.key_callback)
        self._canvas.pack()

        # self.mainloop() #do this in the child classes
        
        # Get the XMLRPC server to start in the background quite soon
        def start_server():
            while not self.server_quit:
                self.server._handle_request_noblock()
        Timer(0.1, start_server).start()

        # Possibly get the window to hide in the background on startup, to be used as an XMLRPC service
        self.hideForServiceMode = serviceMode


    def mouseButton1_callback(self, event):
        self.mouse_callback(event, 1)
        
    def mouseButton2_callback(self, event):
        self.mouse_callback(event, 2)
        
    def mouseButton3_callback(self, event):
        self.mouse_callback(event, 3)

    def mouse_callback(self, event, button):
        #print event
        #hide unhide
        #self._canvas.focus_set()
        print
        print datetime.now(), "BeamGrid base clicked at (%d,%d) using button %d" % (event.x_root, event.y_root, button)
        #TkTransparent.die(self)
        self.hide()
        windowServer.hide()

        # Now that our windows are hidden, pass the mouse click to the window underneath
        def forward_mouse_click():
            print datetime.now(), "Forwarding the mouse button click", button
            btnCode = Button.left
            if button == 2:
                btnCode = Button.middle
            elif button == 3:
                btnCode = Button.right
            mouse.click(btnCode, 1)
        Timer(0.1, forward_mouse_click).start()

        self.clearGridHighlight()


    def setup_xmlrpc_server(self):
        self.server_quit = 0
        print datetime.now(), "Setting up the base XMLRPC mouse grid server at", MOUSE_SERVER_ADDRESS
        self.server = SimpleXMLRPCServer(MOUSE_SERVER_ADDRESS, requestHandler=RequestHandler, allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
        #TODO: Disable this for security when not debugging:
        #self.server.register_introspection_functions()
        self.server.register_function(self.xmlrpc_injectSymbol, "injectSymbol")
        self.server.register_function(self.xmlrpc_injectSymbols, "injectSymbols")
        self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")
        self.server.register_function(self.xmlrpc_move_mouse_relative, "move_mouse_relative")
        self.server.register_function(self.xmlrpc_keypress, "keypress")
        self.server.register_function(self.xmlrpc_showMouseGrid, "showMouseGrid")
        self.server.register_function(self.xmlrpc_moveToCenter, "moveToCenter")


    def xmlrpc_moveToCenter(self):
        print
        print datetime.now(), "BeamGrid base XMLRPC mouse grid server in moveToCenter()"
        self.moveMouse(self.dimensions.width/2, self.dimensions.height/2)

    def xmlrpc_move_mouse(self, x, y):
        print
        print datetime.now(), "BeamGrid base XMLRPC mouse grid server in move_mouse(%d,%d)" % (x, y)
        self.moveMouse(x, y)

    def xmlrpc_move_mouse_relative(self, dx, dy):
        print
        print datetime.now(), "BeamGrid base XMLRPC mouse grid server in move_mouse_relative(%d,%d)" % (dx, dy)
        # Read the current mouse cursor position
        oldMousePosition = mouse.position
        print datetime.now(), "Mouse currently is at: ", oldMousePosition
        mx = oldMousePosition[0] + dx
        my = oldMousePosition[1] + dy

        # Move the actual mouse cursor, using pynput
        print datetime.now(), "Moving mouse cursor to position (%d,%d)" % (mx, my)
        mouse.position = (mx, my)


    def xmlrpc_showMouseGrid(self, gridMode, mouseClick):
        self.mouseGridMode = gridMode
        self.queueMouseClick = mouseClick
        print
        print datetime.now(), "BeamGrid base XMLRPC mouse grid server in showMouseGrid(mode='%s', click=%s)" % (self.mouseGridMode, mouseClick)

        # Allow to show the mouse grid along X, Y or both directions
        self.axis = ''
        if len(self.mouseGridMode) > 0:
            self.axis = self.mouseGridMode[0]

        # Reset the 2D grid stage
        self.gridStage = 0
        self.gridStageX = -1
        self.gridStageY = -1

        # Allow to show the mouse grid on different parts of the screen or different screens
        self.level = 0
        if len(self.mouseGridMode) > 1:
            self.level = int(self.mouseGridMode[1])     # Can be x0, x1, etc

        # Show the mouse grid
        if self.axis == 'x' or self.axis == 'y' or self.axis == 'g':
            # The 2D grid is extremely slow (~1 second!) to render while it's visible, but is fast to render while it's not visible.
            # Clearing the background is also slow.
            # So only clear & render it from scratch if we actually need to modify the content.
            if (self.previousContent != self.axis) or (self.axis == 'g' and self.previousContent == 'g' and self.highlightColumn >= 0):
                print datetime.now(), "Clearing the rendering"
                self.withdraw()     # Stop displaying the window, but don't destroy it
                # Possibly clear the grid display, if a section was being highlighted
                alreadyCleared = self.clearGridHighlight()
                if not alreadyCleared:
                    self._canvas.delete("all")
                self.draw()
                if self.axis == 'x':
                    t = "Full"  # X grid shows lots of symbols
                else:
                    t = "Mini"  # Y grid and 2D only show about half of the symbols
                windowServer.setWindowTitle("InvisibleWindow - " + t)
                self.unhide()       # Display the window onto the screen
                self.deiconify()    # Display the window
            else:
                # This axis is ready for display, so simply display it
                #self.draw()
                self.unhide()       # Display the window onto the screen
        else:
            print datetime.now(), "Unknown axis!", self.axis


    def xmlrpc_injectSymbol(self, event):
        print
        print datetime.now(), "BeamGrid base XMLRPC mouse grid server received symbol injection", event
        #print "PHRASE:", event['phrase']
        self.processCharacter(symbol=event['symbol'])
        #print "DONE."

    def xmlrpc_injectSymbols(self, event1, event2):
        print
        print datetime.now(), "BeamGrid base XMLRPC mouse grid server received symbols injection", event1, event2
        self.processCharacter(symbol=event1['symbol'])
        # Only process the 2nd symbol if we know we're in a 2D grid mode and are accepting 2 inputs
        if event2 and self.axis == 'g' and self.gridStage == 1:
            print datetime.now(), "Processing 2nd symbol that was injected"
            self.processCharacter(symbol=event2['symbol'])
        else:
            print datetime.now(), "Skipping 2nd symbol that was injected, since we're not expecting 2 inputs"


    def xmlrpc_keypress(self, event):
        print datetime.now(), "XMLRPC base mouse grid server received keypress event", event
        # If the user is trying to cancel the grid, make sure we don't queue a mouse click at the end of it
        if event['keysym'] == 'escape':
            self.queueMouseClick = -1
        else:
            # If it's in keyboard mode, allow to click mouse buttons by hitting special keys, since there's no other way to mouse click on a keyboard.
            if self.keyboardMode:
                btnCode = 0
                if event['keysym'] == 'Return':
                    print datetime.now(), "Adding a left mouse click to be performed after the mouse move"
                    btnCode = 1     # Left mouse click
                elif event['keysym'] == 'space':
                    print datetime.now(), "Adding a right mouse click to be performed after the mouse move"
                    btnCode = 3     # Right mouse click
                if btnCode > 0:
                    # Queue the mouse click for later
                    self.queueMouseClick = btnCode
                    return

        # Send a key event
        event2 = KeyEvent(event['char'], event['keysym'], event['keycode'])
        self.key_callback(event2)

    def key_callback(self, event):
        print datetime.now(), "BeamGrid base keyboard event, pressing the key '%s'. keysym='%s', keycode=%s" % (event.char, event.keysym, event.keycode)
        # Send the keyboard character. Except for the rare case such as the "and" (∧) character that InvisibleWindow is sending as a keysym.
        if len(event.char) > 0:
            self.processCharacter(symbol=event.char)
        else:
            self.processCharacter(phrase=event.keysym)


    def hideBothWindows(self):
        # Hide this mouse grid window
        self.hide()

        # Hide the InvisibleWindow (so it doesn't steal keyboard focus) very soon but not yet,
        # otherwise the InvisibleWindow RPC for sending keyboard events might get stuck here!
        def hide_windowServer():
            #windowServer = xmlrpclib.ServerProxy(INVISIBLEWINDOW_SERVER_ADDRESS)
            # Sometimes this causes a "CannotSendRequest" error in xmlrpc lib, even if it works fine,
            # so we wrap it in a try/except block
            try:
                windowServer.hide()
            except:
                pass
        Timer(0.15, hide_windowServer).start()


    # Possibly clear the grid display, if a section was being highlighted
    def clearGridHighlight(self):
        if self.timerMidway:
            self.timerMidway.cancel()
            self.timerMidway = None
            print datetime.now(), "Cancelling the midway highlighting"
        if self.highlightColumn >= 0:
            print datetime.now(), "Clearing the highlighting display"
            self.highlightColumn = -1
            self._canvas.delete("all")
            if self.axis == 'g':
                self.draw_grid2D()
            return True
        return False


    # Handle a character, that was either typed on a keyboard or spoken by voice
    def processCharacter(self, char="", symbol=""):
        #print datetime.now(), "In processCharacter(), axis", self.axis
        closeGrid = False
        if self.axis == 'x' or self.axis == 'y':

            # Calculate the X and Y symbol number for the given typed character or symbol
            c = self.calc1DIndex(symbol=symbol)

            # Move the actual mouse pointer
            (mx, my) = self.getPixelFromChar1D(c)
            self.moveMouse(mx, my)

            # We have processed one axis, now see if we should process another axis.
            print datetime.now(), "Finished processing axis", self.axis

            # Either switch to another mouse grid axis, or hide our 2 windows
            if len(self.mouseGridMode) > 2 and c >= 0:     # mouseGridMode can be something like "x0y0"
                print datetime.now(), "Since mouseGridMode is", self.mouseGridMode, ", we will process the remaining mode now."
                def processNextMode():
                    # Remove the 2 characters of the grid mode that was just processed.
                    self.mouseGridMode = self.mouseGridMode[2:]
                    #self.axis = 'y'
                    #self.axis = 'None'
                    # Occasionally the invisible window seems to hide() and lose focus before switching grid modes.
                    # So let's make sure the invisible window has focus just before we switch modes.
                    windowServer.unhide()
                    print datetime.now(), "Changing to mouseGridMode '%s'" % (self.mouseGridMode)
                    self.xmlrpc_showMouseGrid(self.mouseGridMode, False)
                Timer(0.15, processNextMode).start()
            else:
                closeGrid = True

        elif self.axis == 'g':

            # Calculate the X and Y symbol number for the given typed character or symbol
            c = self.calc1DIndex(symbol=symbol)
            
            if c >= 0:
                # The first letter is for the X axis, the 2nd letter is for the Y axis.
                if self.gridStage == 0:
                    print datetime.now(), "Now that we have the X axis for the 2D grid, prepare for the Y axis."
                    self.gridStageX = c
                    self.gridStage = 1      # Prepare for the next axis
                    
                    # If the user sits in this temporary middle state for a while, highlight the grid to
                    # show that we're in the middle state and they should either cancel, or say one more symbol.
                    def highlightMidway():
                        self._canvas.delete("all")
                        self.highlightColumn = self.gridStageX
                        print datetime.now(), "Highlighting column", self.highlightColumn, "to make sure the user knows they should either cancel or say another symbol"
                        self.draw_grid2D()
                        #self.attributes("-alpha", 0.4)  # Show this whole window as semi-transparent. This line must be after "wait_visibility".
                        self.deiconify()    # Display the window
                        self.timerMidway = None
                    # Keep hold of the threading.Timer object so we can potentially cancel the highlighting later,
                    # if the user does something before we need to highlight it.
                    self.timerMidway = Timer(1.0, highlightMidway)
                    self.timerMidway.start()
                    print datetime.now(), "Starting a timer to eventually show highlighting"
                elif self.gridStage == 1:
                    print datetime.now(), "Now that we have both the X axis and Y axis for the 2D grid, move the actual mouse pointer."
                    self.gridStageY = c

                    (mx, my) = self.getPixelFromChar2D(self.gridStageX, self.gridStageY)

                    # Now that we have both the X and Y value, move the actual mouse pointer
                    self.moveMouse(mx, my)
                    
                    closeGrid = True
            else:
                # They probably cancelled the grid or made a mistake, so close the grid.
                closeGrid = True

        if closeGrid:
            print datetime.now(), "Finished processing axis", self.axis
            self.hideBothWindows()
            self.gridStage = 0      # Reset

            # Possibly clear the grid display, if a section was being highlighted
            self.clearGridHighlight()

            # Possibly press a mouse button that has been scheduled to happen after the mouse has been moved
            if self.queueMouseClick > 0:
                print datetime.now(), "Performing the queued mouse button", self.queueMouseClick, "click"
                btnCode = Button.left
                if self.queueMouseClick == 2:
                    btnCode = Button.middle
                elif self.queueMouseClick == 3:
                    btnCode = Button.right
                mouse.click(btnCode, 1)
                self.queueMouseClick = -1


    def pre_redraw(self):
        '''gets the window ready to be redrawn'''
        self.deiconify()    # Displays the window. Only needed if you have used iconify or withdraw
        self._canvas.delete("all")

    def unhide(self):
        ''''''
        self.deiconify()    # Display the window
        self.lift()
        time.sleep(0.1)
        self.focus_force()
        self.focus_set()
        self.focus()

    def hide(self):
        self.withdraw()     # Stop displaying the window, but don't destroy it

    def xmlrpc_kill(self):
        print datetime.now(), "XMLRPC base mouse grid server received kill event"
        self.after(2, self.die)

    def die(self):
        print datetime.now(), "Closing the base grid"
        self.server_quit = 1
        self.destroy()
        # Kill the 2 grid windows, and wait till the signal has been dispatched.
        #subprocess.call("pkill -f -9 standalone_grids.py", shell=True)
        subprocess.call("pkill -f -9 invisibleWindow.py", shell=True)
        os.kill(os.getpid(), signal.SIGTERM)
        import sys
        sys.exit()

    @staticmethod
    def move_mouse(mx, my):
        win32api.SetCursorPos((mx, my))


class RainbowGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None, square_alpha=None, axis='Ignored', serviceMode=False, keyboardMode=False):
        '''square_size is an integer'''
        TkTransparent.__init__(self, "Rainbow", grid_size)
        self.attributes("-alpha", 0.5)
        self.square_size = 37 #square_size if square_size else 37
        self.square_alpha = 125 #square_alpha if square_alpha else 125
        print "RainbowGrid using a square_size of", self.square_size
        self.colors = [
            (255, 0, 0, self.square_alpha),  # red
            (187, 122, 0, self.square_alpha),  # orange 255, 165, 0
            (255, 255, 0, self.square_alpha),  # yellow
            (0, 128, 0, self.square_alpha),  # green
            (0, 0, 125, self.square_alpha),  # blue
            (128, 0, 128, self.square_alpha)  # purple
        ]
        self.position_index = None

        self.info_pre = 0
        self.info_color = 0
        self.info_num = 0

        self.refresh()
        self.mainloop()

    def refresh(self):
        '''thread safe'''
        self.hide()
        self.after(10, self.draw)

    def finalize(self):
        self.imgtk = ImageTk.PhotoImage(self.img)
        self._canvas.create_image(
            self.dimensions.width/2, self.dimensions.height/2, image=self.imgtk)

    def setup_xmlrpc_server(self):
        TkTransparent.setup_xmlrpc_server(self)
        #self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")

    def xmlrpc_move_mouse(self, pre, color, num):
        if pre > 0:
            pre -= 1
        selected_index = self.position_index[color + pre*len(self.colors)][num]
        self.move_mouse(selected_index[0] + self.dimensions.x,
                        selected_index[1] + self.dimensions.y)

    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width/self.square_size) + 2):
                self.xs.append(x*self.square_size)
            for y in range(0, int(self.dimensions.height/self.square_size) + 2):
                self.ys.append(y*self.square_size)
        self.position_index = []
        # add first "color":
        self.position_index.append([])

    def draw(self):
        self.pre_redraw()
        #self.img = ImageGrab.grab([
        #    self.dimensions.x, self.dimensions.y,
        #    self.dimensions.x + self.dimensions.width,
        #    self.dimensions.y + self.dimensions.height
        #])  # .filter(ImageFilter.BLUR)
        self.draw_squares()
        self.finalize()
        self.unhide()

    def draw_squares(self):
        self.fill_xs_ys()
        #

        text_background_buffer = int(self.square_size/6)
        xs_size = len(self.xs)
        ys_size = len(self.ys)
        box_number = 0
        colors_index = 0
        font = ImageFont.truetype("arialbd.ttf", 15)
        draw = ImageDraw.Draw(self.img, 'RGBA')

        for ly in range(0, ys_size - 1):
            for lx in range(0, xs_size - 1):
                txt = str(box_number)
                tw, th = draw.textsize(txt, font)
                text_x = int((self.xs[lx] + self.xs[lx + 1] - tw)/2) + 1
                text_y = int((self.ys[ly] + self.ys[ly + 1] - th)/2) - 1
                draw.rectangle(
                    [
                        self.xs[lx] + text_background_buffer,
                        self.ys[ly] + text_background_buffer,
                        self.xs[lx + 1] - text_background_buffer,
                        self.ys[ly + 1] - text_background_buffer
                    ],
                    fill=self.colors[colors_index],
                    outline=False)

                draw.text((text_x + 1, text_y + 1), txt, (0, 0, 0), font=font)
                draw.text((text_x - 1, text_y + 1), txt, (0, 0, 0), font=font)
                draw.text((text_x + 1, text_y - 1), txt, (0, 0, 0), font=font)
                draw.text((text_x - 1, text_y - 1), txt, (0, 0, 0), font=font)
                draw.text((text_x, text_y), txt, (255, 255, 255), font=font)
                # index the position
                self.position_index[len(self.position_index) - 1].append(
                    (int((self.xs[lx] + self.xs[lx + 1])/2),
                     int((self.ys[ly] + self.ys[ly + 1])/2)))

                # update for next iteration
                box_number += 1
                if box_number == 100:
                    # next color
                    box_number = 0
                    colors_index += 1
                    colors_index %= len(self.colors)  # cycle colors
                    self.position_index.append([])

        del draw


class DouglasGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None, axis='Ignored', serviceMode=False, keyboardMode=False):
        TkTransparent.__init__(self, "DouglasGrid", grid_size)
        self.square_size = square_size if square_size else 25
        print "DouglasGrid using a square_size of", self.square_size

        self.draw()
        self.mainloop()

    def setup_xmlrpc_server(self):
        TkTransparent.setup_xmlrpc_server(self)
        #self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")

    def xmlrpc_move_mouse(self, x, y):
        DouglasGrid.move_mouse(
            x*self.square_size + int(self.square_size/2) + self.dimensions.x,
            y*self.square_size + int(self.square_size/2) + self.dimensions.y)

    def draw(self):
        self.pre_redraw()
        self.draw_lines_and_numbers()
        self.unhide()

    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width/self.square_size) + 2):
                self.xs.append(x*self.square_size)
            for y in range(0, int(self.dimensions.height/self.square_size)):
                self.ys.append(y*self.square_size)

    def draw_lines_and_numbers(self):

        self.fill_xs_ys()

        text_background_buffer = int(self.square_size/10)
        xs_size = len(self.xs)
        for lx in range(0, xs_size):
            fill = "black"
            if lx % 3:
                fill = "gray"
            self._canvas.create_line(
                self.xs[lx], 0, self.xs[lx], self.dimensions.height, fill=fill)
            if lx + 1 < xs_size:
                self._canvas.create_rectangle(
                    self.xs[lx] + text_background_buffer,
                    0 + text_background_buffer,
                    self.xs[lx + 1] - text_background_buffer,
                    self.square_size - text_background_buffer,
                    fill='Black')
                self._canvas.create_rectangle(
                    self.xs[lx] + text_background_buffer,
                    self.dimensions.height - self.square_size + text_background_buffer,
                    self.xs[lx + 1] - text_background_buffer,
                    self.dimensions.height - text_background_buffer,
                    fill='Black')
                text_x = int((self.xs[lx] + self.xs[lx + 1])/2)
                self._canvas.create_text(
                    text_x,
                    int(self.square_size/2),
                    text=str(lx),
                    font="Arial 10 bold",
                    fill='White')
                self._canvas.create_text(
                    text_x,
                    self.dimensions.height - int(self.square_size/2),
                    text=str(lx),
                    font="Arial 10 bold",
                    fill='White')

        ys_size = len(self.ys)
        for ly in range(0, ys_size):
            fill = "black"
            if ly % 3:
                fill = "gray"
            self._canvas.create_line(
                0, self.ys[ly], self.dimensions.width, self.ys[ly], fill=fill)
            if ly + 1 < ys_size and ly != 0:
                self._canvas.create_rectangle(
                    0 + text_background_buffer,
                    self.ys[ly] + text_background_buffer,
                    self.square_size - text_background_buffer,
                    self.ys[ly + 1] - text_background_buffer,
                    fill='Black')
                self._canvas.create_rectangle(
                    self.dimensions.width - self.square_size + text_background_buffer,
                    self.ys[ly] + text_background_buffer,
                    self.dimensions.width - text_background_buffer,
                    self.ys[ly + 1] - text_background_buffer,
                    fill='Black')
                text_y = int((self.ys[ly] + self.ys[ly + 1])/2)
                self._canvas.create_text(
                    int(self.square_size/2),
                    text_y,
                    text=str(ly),
                    font="Arial 10 bold",
                    fill='White')
                self._canvas.create_text(
                    self.dimensions.width - int(self.square_size/2),
                    text_y,
                    text=str(ly),
                    font="Arial 10 bold",
                    fill='White')


# For 1D grids: Show a fullscreen grid with single character wide columns or rows, so you say something like "five" for column 5.
# For 2D grids: Show a fullscreen grid with 2-character boxes, so you say something like "5 3" for cell 5 across and 3 down.
class BeamGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None, level=0, axis='x', serviceMode=False, keyboardMode=False):
        TkTransparent.__init__(self, "BeamGrid", grid_size, serviceMode=serviceMode, keyboardMode=keyboardMode)
        self.axis = axis
        self.level = level
        self.previousContent = 'None'
        self.keyboardMode = keyboardMode

        # Reset the 2D grid stage
        self.gridStage = 0
        self.gridStageX = -1
        self.gridStageY = -1

        # Set up the geometry
        if square_size == None:
            square_size = 22    # Default for 2D grids. Not used for 1D grids.
        self.cellWidth = square_size
        self.cellHeight = square_size - 4   # Squeeze a bit more cells vertically
        self.fontString = fontFamily + " " + str(fontSize) + " " + fontWeight
        self.fontObject = tkfont.Font(family=fontFamily, size=fontSize, weight=fontWeight)
        self.charWidth = self.fontObject.measure("0")
        self.charHeight = self.fontObject.metrics("linespace")
        print datetime.now(), "BeamGrid using a square_size of", self.cellWidth, "x", self.cellHeight, "on a screen size of", self.dimensions.width, "x", self.dimensions.height

        # If the measurements above don't work on your system, you can hardcode charWidth & charHeight here.
        # eg: On Linux Mint 19 Cinnamon, font 'Monospace 10 normal' is 10x19 pixels for each character.
        #charWidth = 10
        #charHeight = 19
        self.charHeight = self.charHeight - 4
        print datetime.now(), "Character size for font (", self.fontString, ") is", self.charWidth, "x", self.charHeight, "pixels"

        # Get the number of characters that would fit on the screen (rounded up)
        self.xs_size = int((self.dimensions.width + self.charWidth) / self.charWidth)
        self.ys_size = int((self.dimensions.height + self.charHeight) / self.charHeight)

        # Render
        self.pre_redraw()
        self.draw()
        windowServer.setWindowTitle("InvisibleWindow - 1D")  # Initialize the titlebar for the initial grid mode, to support cached info in showMouseGrid()
        #self.unhide()       # Display the window onto the screen
        print datetime.now(), "Rendering the BeamGrid window"
        self.mainloop()


    def draw(self):
        #self.pre_redraw()
        if self.axis == 'x':
            self.draw_gridX()
        elif self.axis == 'y':
            self.draw_gridY()
        elif self.axis == 'g':
            self.draw_grid2D()

        # Possibly get the window to hide in the background on startup, to be used as an XMLRPC service
        if self.hideForServiceMode:
            self.deiconify()    # Display the window
            self.hide()
            self.hideForServiceMode = False

        # Keep track of the axis that was last displayed, so we won't need to clear it out to render it again.
        self.previousContent = self.axis


    def draw_gridX(self):
        # Rendering all rows as a single multi-line string is likely to run faster than rendering each line one at a time,
        # but since TK on some OSes (eg: Linux X Windows) adds 1 or 2 pixels of extra padding above and below each line,
        # we will get more densely packed text if we render each line separately, without the padding.
        print datetime.now(), "Number of characters that fit on the screen:", self.xs_size-1, "x", self.ys_size-1
        self.gridWidth = len(self.charsString) * self.charWidth
        self.gridHeight = self.ys_size * self.charHeight
        numGridsWide = int((self.dimensions.width + self.gridWidth - 1) / self.gridWidth)
        numGridsHigh = int((self.dimensions.height + self.gridHeight - 1) / self.gridHeight)
        print datetime.now(), "Number of grids:", numGridsWide, "x", numGridsHigh, ". grid level: ", self.level
        if numGridsWide > len(textColors):
            print datetime.now(), "ERROR: Screen is too big for your font size! Please use smaller font size (charWidth and charHeight)!"
            #sys.exit(1)

        # Render the whole grid of text, one row at a time
        gx = self.level
        #for gx in range(0, numGridsWide):
        if gx >= 0 and gx < numGridsWide:
            gy = 0
            offsetX = 0
            offsetY = -3
            for ly in range(0, self.ys_size-1):
                text_x = (offsetX) + (gx * self.gridWidth )
                text_y = (offsetY) + (gy * self.gridHeight) + (ly * self.charHeight)
                self._canvas.create_text(
                    text_x,
                    text_y,
                    text=self.charsString,
                    #font="Arial 10 bold",
                    font=self.fontObject,
                    anchor=tk.NW,   # Measure from the top-left
                    #anchor=tk.CENTER,
                    fill=textColors[gx])


    def draw_gridY(self):
        # Rendering all rows as a single multi-line string is likely to run faster than rendering each line one at a time,
        # but since TK on some OSes (eg: Linux X Windows) adds 1 or 2 pixels of extra padding above and below each line,
        # we will get more densely packed text if we render each line separately, without the padding.
        print datetime.now(), "Number of characters that fit on the screen:", self.xs_size-1, "x", self.ys_size-1
        numRows = min(self.ys_size, len(self.charsString))    # Try to fit all characters down the screen, but the screen might be too small
        self.gridWidth = self.xs_size * self.charWidth
        self.gridHeight = numRows * self.charHeight
        numGridsWide = int((self.dimensions.width + self.gridWidth - 1) / self.gridWidth)
        numGridsHigh = int((self.dimensions.height + self.gridHeight - 1) / self.gridHeight)
        print datetime.now(), "Number of grids:", numGridsWide, "x", numGridsHigh, ". grid level: ", self.level
        if numGridsHigh > len(textColors):
            print datetime.now(), "ERROR: Screen is too big for your font size! Please use smaller font size (charWidth and charHeight)!"
            #sys.exit(1)

        # Render the whole grid of text, one row at a time
        gy = self.level
        #for gy in range(0, numGridsHigh):
        if gy >= 0 and gy < numGridsHigh:
            gx = 0
            offsetX = 0
            offsetY = -3
            for ly in range(0, numRows-1):
                rowString = self.charsString[ly] * self.xs_size   # Generate a row full of a single character
                text_x = (offsetX) + (gx * self.gridWidth )
                text_y = (offsetY) + (gy * self.gridHeight) + (ly * self.charHeight)
                self._canvas.create_text(
                    text_x,
                    text_y,
                    text=rowString,
                    #font="Arial 10 bold",
                    font=self.fontObject,
                    anchor=tk.NW,   # Measure from the top-left
                    #anchor=tk.CENTER,
                    fill=textColors[gy])


    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width/self.cellWidth) + 2):
                self.xs.append(x*self.cellWidth)
            for y in range(0, int(self.dimensions.height/self.cellHeight) + 2):
                self.ys.append(y*self.cellHeight)

    def draw_grid2D(self):
        self.fill_xs_ys()
        #print "square_size = ", self.square_size, self.xs, self.ys, self.dimensions.width, self.dimensions.height

        gridColor = "gray"
        if self.gridStage == 1:
            gridColor = "green"

        self.gridWidth = self.cellWidth * len(self.charsString)
        self.gridHeight = self.cellHeight * len(self.charsString)
        
        # Draw the grid bars
        xs_size = len(self.xs)
        ys_size = len(self.ys)
        print datetime.now(), "Number of symbols we can shown on the screen:", xs_size-1, "x", ys_size-1

        for lx in range(0, xs_size):
            fill = "black"
            if lx % 3:
                fill = gridColor
            self._canvas.create_line(
                self.xs[lx], 0, self.xs[lx], self.dimensions.height, fill=fill)
        for ly in range(0, ys_size):
            fill = "black"
            if ly % 3:
                fill = gridColor
            self._canvas.create_line(
                0, self.ys[ly], self.dimensions.width, self.ys[ly], fill=fill)

        xs_size = min(xs_size, len(self.charsString))
        ys_size = min(ys_size, len(self.charsString))
        
        #text_background_buffer = int(self.square_size/10)

        # Draw the text. Since we're calling 'create_text' for each cell, this code is quite slow, especially if
        # the window is visible (causing a screen repaint for each cell!!)
        for ly in range(0, ys_size):
            for lx in range(0, xs_size):
                if self.highlightColumn < 0 or self.highlightColumn == lx:
                    if lx + 1 < xs_size and ly + 1 < ys_size:
                        text_x = int((self.xs[lx] + self.xs[lx + 1])/2) + self.level * self.gridWidth
                        text_y = int((self.ys[ly] + self.ys[ly + 1])/2)
                        self._canvas.create_text(
                            text_x,
                            text_y,
                            text=self.charsString[lx % len(self.charsString)] + self.charsString[ly % len(self.charsString)],
                            #font="Arial 10 bold",
                            font=self.fontObject,
                            #anchor=tk.NW,   # Measure from the top-left
                            anchor=tk.CENTER,
                            fill=textColors[0])


    # Calculate the symbol index for the given character (if provided) or phrase
    def calc1DIndex(self, symbol="", phrase=""):
        #print datetime.now(), self.charsDict
        # Get the character position they said
        if len(symbol) > 0:
            # For plain keyboard letters such as 'a', search by the letter, not the spoken phrase.
            #c = self.charsString.find(char)
            try:
                c = self.charsDict.values().index(symbol) # Replace with list(self.charsDict.keys()).index(symbol) for Python 3
            except:
                print datetime.now(), u"Couldn't find symbol", symbol
                c = -1
            if c >= 0:
                print datetime.now(), u"They said character", symbol.encode('utf-8'), u"=", c
            else:
                print datetime.now(), u"Couldn't find character", symbol.encode('utf-8')
                return -1
        elif len(phrase) > 0:
            # For custom symbols, search for the spoken phrase.
            #c = self.charsString.find(phrase)
            try:
                c = self.charsDict.keys().index(phrase) # Replace with list(self.charsDict.keys()).index(phrase) for Python 3
            except:
                print datetime.now(), u"Couldn't find phrase", phrase
                return -1
            print datetime.now(), u"They said", phrase, u"which appears as", self.charsDict[phrase], u"at position", c
        else:
            print datetime.now(), "ERROR: Need either a symbol or a phrase!"
            return -1
        return c


    def getPixelFromChar1D(self, c):
        print datetime.now(), "Mouse grid mode is currently:", self.axis, ". Grid level is:", self.level

        # Move either in x or y direction
        mx = -1
        my = -1
        if self.axis == "y":
            # Get the screen pixel coord.
            my = int((c + 0.5) * self.charHeight + 0.5) + (self.level * self.gridHeight)
            return (mx, my)
        elif self.axis == "x":
            # Get the screen pixel coord.
            mx = int((c + 0.5) * self.charWidth + 0.5) + (self.level * self.gridWidth)
            return (mx, my)
        else:
            print datetime.now(), "ERROR in standalone_grids.py: Unknown mouse axis!"
            return (-1, -1)
        if mx < 0 and my < 0:
            print datetime.now(), "ERROR in standalone_grids.py on server: Unknown mouse input!"
            return (-1, -1)


    def getPixelFromChar2D(self, cx, cy):
        # Get the screen pixel coord for the cell with the 2 given characters
        mx = int((cx + 0.5) * self.cellWidth + 0.5) + (self.level * self.gridWidth)   # Assume level is only horizontal
        my = int((cy + 0.5) * self.cellHeight + 0.5) + 0
        return (mx, my)


    def moveMouse(self, mx, my):
        # Read the current mouse cursor position, to allow moving in just 1 direction
        oldMousePosition = mouse.position
        print datetime.now(), "Mouse currently is at: ", oldMousePosition
        if mx < 0:
            mx = int(oldMousePosition[0])
        if my < 0:
            my = int(oldMousePosition[1])

        # Move the actual mouse cursor, using pynput
        print datetime.now(), "Moving mouse cursor to position (%d,%d)" % (mx, my)
        mouse.position = (mx, my)



def main(argv):
    help_message =  "Usage: grids.py -g <GRID_TYPE> [-m <MONITOR>] [-s|-v [-k|-u]] [-c <CELL_SIZE>]\n" \
                    "where <GRID_TYPE> is one of:\n" \
                    "  r\t rainbow grid\n" \
                    "  d\t douglas grid\n" \
                    "  g\t 2D grid\n" \
                    "  x or y\t 1D grid\n" \
                    "  x0y0\t 1D x grid followed by 1D y grid\n" \
                    "where CELL_SIZE should be 10-100\n" \
                    "other flags:\n" \
                    "-s\t enables service mode\n" \
                    "-v\t disables service mode\n" \
                    "-k\t enables keyboard-only symbols\n" \
                    "-u\t disables keyboard-only symbols\n" \
                    ""
    try:
        opts, args = getopt.getopt(argv, "hg:m:svkuc:")
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    g = None
    m = 1
    level = 0
    axis = 'x'
    serviceMode = False
    keyboardMode = False
    square_size = None

    #print "opts", opts
    for opt, arg in opts:
        #print "opt", opt
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt == '-g':
            if arg == "r":
                g = RainbowGrid
            elif arg == 'd':
                g = DouglasGrid
            elif arg[0] == 'g':
                g = BeamGrid
                axis = arg[0]
                #if len(opts[0]) > 1 and len(opts[0][1]) > 1:
                #opt = opts[0][1]
                if len(arg) > 1:
                    level = int(arg[1])     # Can be g0, g1, etc
            elif arg[0] == 'x':
                g = BeamGrid
                axis = arg[0]
                if len(arg) > 1:
                    level = int(arg[1])     # Can be x0, x1, etc
            elif arg[0] == 'y':
                g = BeamGrid
                axis = arg[0]
                if len(arg) > 1:
                    level = int(arg[1])     # Can be y0, y1, etc
            #print "done -g"
        elif opt == '-m':
            m = arg
        elif opt == '-s':
            print datetime.now(), "Enabling service mode"
            serviceMode = True
        elif opt == '-k':
            print datetime.now(), "Enabling keyboard mode"
            keyboardMode = True
        elif opt == '-c':
            square_size = int(arg)

    if g is None:
        raise ValueError("Grid mode not specified.")

    grid_size = Dimensions(1920, 1080, 0, 0)
    g(grid_size=grid_size, square_size=square_size, level=level, axis=axis, serviceMode=serviceMode, keyboardMode=keyboardMode)


if __name__ == '__main__':
    print datetime.now(), "Creating a grid window"
    main(sys.argv[1:])


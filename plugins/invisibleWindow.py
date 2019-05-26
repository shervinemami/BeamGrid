# coding: utf-8
# Open a normal window (including the full window frame) that's added to the OS window list and taskbar, but make this window invisible.
# Allows a fullscreen frameless window to be displayed on top, with keyboard events being passed to this window, and being part of the OS window list.
# By Shervin Emami 2019 (http://www.shervinemami.info)

# This line is different for Python 2 vs 3:
from Tkinter import Tk

from datetime import datetime
import subprocess
import time
import sys
from threading import Timer
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib

# Allow passing any keypresses to the mouse grid window, since it's a root window that can't receive keypresses
MOUSE_SERVER_ADDRESS = 'http://192.168.56.1:8000'           # Set up our client address
# Allow bringing the invisible window to the front or back of the window stack
INVISIBLEWINDOW_SERVER_ADDRESS = ("192.168.56.1", 8001)     # Set up our server address


# Create the window here, so it can be accessed easily by all functions
root = Tk()


try:
    print datetime.now(), "- InvisibleWindow connecting to XMLRPC mouse server at", MOUSE_SERVER_ADDRESS
    mouseServer = xmlrpclib.ServerProxy(MOUSE_SERVER_ADDRESS)
except e, v:
    print e, v
    raise

class KeyEvent:
    def __init__(self, char, keysym, keycode):
        self.char = char
        self.keysym = keysym
        self.keycode = keycode


def key_callback(event):
    print
    print datetime.now(), "- InvisibleWindow keyboard event, pressing the key '%s'. keysym='%s', keycode=%s" % (event.char, event.keysym, event.keycode)

    # Some special keys like 'Esc' cause problems when sending over XMLRPC. Convert to a spacebar that will get ignored later.
    if event.keysym == 'Escape':
        event.char = ' '
        event.keysym = 'space'
        event.keycode = 65
    # If they said "And" but it sounded like "End", something we don't show in our mouse grid, convert "End" to "And"
    if event.keysym == 'End':
        event.char = ''
        event.keysym = 'and'
        event.keycode = -1

    # Print list of available methods
    #print "SERVER methods:"
    #print mouseServer.system.listMethods()
    
    if len(event.char) == 1:
        keyEvent = KeyEvent(event.char, event.keysym, event.keycode)
        mouseServer.keypress(keyEvent)
    else:
        print datetime.now(), "- Discarding this key event."
    print datetime.now(), "- InvisibleWindow keyboard event is done."

    # Kill the 2 grid windows, and wait till the signal has been dispatched.
    #subprocess.call("pkill -f -9 standalone_grids.py", shell=True)
    ##subprocess.call("pkill -f -9 createInvisibleWindow.py", shell=True)
    #import sys
    #sys.exit()


def mouse_callback(event):
    print datetime.now(), "- InvisibleWindow mouse event at", event.x, event.y
    hide()
    print datetime.now(), "- InvisibleWindow mouse event is done."
    ## Kill the 2 grid windows, and wait till the signal has been dispatched.
    #subprocess.call("pkill -f -9 standalone_grids.py", shell=True)
    ##subprocess.call("pkill -f -9 createInvisibleWindow.py", shell=True)
    #import sys
    #sys.exit()


def unhide():
    print datetime.now(), "- In InvisibleWindow unhide()"
    root.deiconify()    # Display the window
    root.lift()
    time.sleep(0.1)
    root.focus_force()
    root.focus_set()
    print datetime.now(), "- InvisibleWindow unhide is done."


def hide():
    print datetime.now(), "- In InvisibleWindow hide()"
    root.withdraw()     # Stop displaying the window, but don't destroy it
    print datetime.now(), "- InvisibleWindow hide is done."


# Restrict XMLRPC server to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def setup_xmlrpc_server():
    server_quit = 0
    print datetime.now(), "- Setting up the InvisibleWindow XMLRPC server at", INVISIBLEWINDOW_SERVER_ADDRESS
    windowServer = SimpleXMLRPCServer(INVISIBLEWINDOW_SERVER_ADDRESS, requestHandler=RequestHandler, allow_none=True)
    windowServer.register_function(xmlrpc_kill, "kill")
    windowServer.register_function(hide, "hide")
    windowServer.register_function(unhide, "unhide")
    #TODO: Disable this for security when not debugging:
    #windowServer.register_introspection_functions()
    return windowServer


def xmlrpc_kill():
    print datetime.now(), "- XMLRPC InvisibleWindow server received kill event"
    after(2, die)

def die():
    print datetime.now(), "- Closing the InvisibleWindow"
    server_quit = 1
    destroy()
    # Kill the 2 grid windows, and wait till the signal has been dispatched.
    subprocess.call("pkill -f -9 standalone_grids.py", shell=True)
    #subprocess.call("pkill -f -9 createInvisibleWindow.py", shell=True)
    os.kill(os.getpid(), signal.SIGTERM)
    import sys
    sys.exit()


def createInvisibleWindow(argv):
    #root = Tk()
    root.wm_title("InvisibleWindow")
    root.geometry("1x1+0+0")    # Make a tiny window, that wouldn't be noticeable anyway (for systems that don't support transparent windows)
    root.wait_visibility(root)
    # Show this whole window as invisible. This line must be after "wait_visibility".
    #root.wm_attributes('-alpha', 0.0)
    #root.attributes("-alpha", 0.0)

    windowServer = setup_xmlrpc_server()

    # Close this window if any mouse or keyboard events happen.
    root.bind("<Button-1>", mouse_callback)
    root.bind("<Button-2>", mouse_callback)
    root.bind("<Button-3>", mouse_callback)
    root.bind("<KeyPress>", key_callback)

    root.protocol("WM_DELETE_WINDOW", xmlrpc_kill)

    # Get the XMLRPC server to start in the background quite soon
    server_quit = 0
    def start_server():
        while not server_quit:
                windowServer._handle_request_noblock()
    Timer(0.3, start_server).start()

    #serviceMode = False
    if len(argv) > 0 and argv[0] == '-s':
        # serviceMode = True
        # Hide this window from the system taskbar until we're actually needing it
        hide()

    print datetime.now(), "- Rendering invisible window now"
    root.mainloop()


if __name__ == '__main__':
    print datetime.now(), "- Creating an invisible window that includes invisible frame borders"
    createInvisibleWindow(sys.argv[1:])

# Aenea plugin for a keyboard & mouse macro recording & playback system.
# By Shervin Emami (www.shervinemami.info), 2019.

from yapsy.IPlugin import IPlugin
from pathvalidate import sanitize_filename
from pynput.keyboard import Key, KeyCode, Controller
import subprocess
import collections
import codecs

def updateRecognition(label, security_token):
    '''RPC command '''
    print "In updateRecognition(label =", label, ") aenea server plugin."
    pid = -1

    # Load the whole file (if it exists) as unicode into a deque of row strings
    queue = collections.deque([], 10)
    filename = "/tmp/dragon-state.txt"
    lastLine = ""
    f = None
    try:
        f = codecs.open(filename, 'r', encoding='utf-8')
    except:
        pass
    #with open(filename, "r", encoding='utf-8') as f:
    if f:
        for line in f:
            line = line.rstrip('\n')    # Remove the trailing newline character
            lastLine = line
            #print u"loaded ", line
            queue.append(line)
        f.close()

    # If we have a valid string but the previous string was a bad recognition, then overwrite that previous string.
    if lastLine == "..." or lastLine == "<???>":
        queue.pop()

    # Add the new item to the end of the queue
    queue.append(label)
    #print queue

    # Now store the deque back to the file!
    f = codecs.open(filename, 'w', encoding='utf-8')
    if f:
        for line in queue:
            f.write(line + u'\n')
        f.close()

    return pid


class UpdateRecognitionPlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(updateRecognition)

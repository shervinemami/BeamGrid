from yapsy.IPlugin import IPlugin
import subprocess
import codecs
import collections

def loadRecognitionHistory():
    # Load the whole file as unicode into a deque of row strings, in reverse order
    queue = collections.deque()
    filename = "/tmp/dragon-state.txt"
    f = codecs.open(filename, 'r', encoding='utf-8')
    #with open(filename, "r", encoding='utf-8') as f:
    numLines = 0
    if f:
        for line in f:
            #line = line.rstrip('\n')    # Remove the trailing newline character

            # Skip the line, if it's related to history or processing
            blacklist = ["...\n", "<???>\n", "history\n"]
            if line in blacklist:
                continue

            #print u"loaded ", line
            queue.appendleft(line)
            numLines += 1
        f.close()
    print "History of length", numLines, "is", queue
    return queue


def showHistory(security_token):
    '''RPC command '''
    print "In showHistory() aenea server plugin."
    pid = -1
    # Create a background process to run the script and return here straight away.
    #pid = subprocess.Popen(["/Core/Custom/showRecognitionHistory.sh"]).pid
    
    queue = loadRecognitionHistory()

    # Generate a multi-line string from the queue, with numbered rows
    counter = 1
    string = ""
    for line in queue:
        string += "%2d: %s" % (counter, line)
        counter += 1
    #print string

    # Create a background process to show a notification
    pid = subprocess.Popen(["zenity", "--notification", "--timeout=4", "--text=Recognition History:\n" + string]).pid

    return pid


class ShowHistoryPlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(showHistory)

if __name__ == '__main__':
    showHistory("")

from yapsy.IPlugin import IPlugin

import subprocess

enabled = True
pid = -1

def clickMouseGrid(button, security_token):
    '''RPC command '''
    print "In clickMouseGrid(", button, ") aenea server plugin."
    # Stop the grid script, and wait until it has stopped before continuing.
    subprocess.call("plugins/clickMouseGrid.sh %d" % (button), shell=True)
    pid = -1        


class ClickMouseGridPlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(clickMouseGrid)

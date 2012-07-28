from twisted.web.client import getPage
from twisted.internet import reactor

#------------------------------------------------------------------------------
class VeraTwistedDispatcher:

    def __init__(self):
        self.callback = []

    #----------------------------
    # grabs url, calls callback when load is done
    def fetch(self, url, callback):
        d = getPage(url)
        d.addCallback(callback)

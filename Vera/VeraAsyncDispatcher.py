import asyncore
import string, socket
import StringIO
import mimetools, urlparse
import SimpleAsyncHTTP

#------------------------------------------------------------------------------
class VeraAsyncDispatcher:

    def __init__(self):
        self.temp_data = ''
        self.callback = []

    #----------------------------
    # grabs url, calls callback when load is done
    def fetch(self, url, callback):
        self.callback = callback
        SimpleAsyncHTTP.AsyncHTTP(url, self)

    #----------------------------
    # These Three Class Required by AsyncHTTP
    def http_header(self, request):
        pass
        # handle header
        #if request.status is None:
        #    print "connection failed"
        #else:
        #    print "status", "=>", request.status
        #    for key, value in request.header.items():
        #        print key, "=", value

    def feed(self, data):
        self.temp_data += data

    def close(self):
        self.callback(self.temp_data)
        self.temp_data = ''
    # End req by AsyncHTTP
    #----------------------------
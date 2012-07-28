from VeraClient import *
from VeraTwistedDispatcher import *

def veraCallback(str):
    print str

ip = "192.168.1.xxx"
dispatcher = VeraTwistedDispatcher()
consumer   = VeraClient(ip, veraCallback, dispatcher)

reactor.run()

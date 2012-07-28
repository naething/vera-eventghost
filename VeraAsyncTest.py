

from VeraClient import *
from VeraAsyncDispatcher import *

def veraCallback(str):
    print str

ip = "192.168.1.xxx"
dispatcher = VeraAsyncDispatcher()
consumer   = VeraClient(ip, veraCallback, dispatcher)
asyncore.loop()

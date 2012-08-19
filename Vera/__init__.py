import eg
import urllib
import json

from VeraClient import *
from VeraDevice import *
from VeraAsyncDispatcher import *

eg.RegisterPlugin(
    name = "MiCasaVerde Vera",
    author = "Rick Naething",
    version = "0.0.3",
    kind = "other",
    description = "Control Over Devices on Vera"
)

#-----------------------------------------------------------------------------
class Vera(eg.PluginBase):

    def __init__(self):
        self.AddAction(SetSwitchPower)
        self.AddAction(SetDimming)
        self.AddAction(RunScene)
        self.HTTP_API   = VERA_HTTP_API()
        self.dispatcher = VeraAsyncDispatcher()
        self.vera       = []
        eg.RestartAsyncore()

    def Configure(self, ip="127.0.0.1", port="3480"):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, ip)
        textControl2 = wx.TextCtrl(panel, -1, port)
        panel.sizer.Add(wx.StaticText(panel, -1, "IP address of Vera"))
        panel.sizer.Add(textControl)
        panel.sizer.Add(textControl2)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(), textControl2.GetValue())

    def __start__(self, ip='127.0.0.1', port='3480'):
        self.ip = ip
        self.port = port
        self.HTTP_API.connect(ip=ip, port=port)
        self.vera       = VeraClient(ip, self.veraCallback, self.dispatcher)

    def __stop__(self):
        pass

    def __close__(self):
        pass            
        
    def veraCallback(self, msg, state=tuple()):
        # msg is either a string or a VeraDevice
        if isinstance(msg, VeraDevice):
            event = self.vera.rooms[msg.room] + '.' + str(msg)
        else:
            event = msg
        self.TriggerEvent(event)
    

#-----------------------------------------------------------------------------      
class VERA_HTTP_API:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "3480"
        return

    def connect(self, ip=None, port=None):
        if ip: self.ip = ip
        if port: self.port = port
        print 'HTTP API connected'

    def send(self, url):
        try:
            responce = urllib.urlopen('http://'+self.ip+':'+self.port+url).readlines()
        except IOError:
            eg.PrintError('HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+ url)
        else:
            return

    def close(self):
        print 'HTTP API connection closed'

#-----------------------------------------------------------------------------
class RunScene(eg.ActionBase):
    name = "Run Scene"
    description = "Runs a Vera Scene"

    def __call__(self, device):
        print "Running Scene " + str(device)
        url = "/data_request?id=lu_action&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1&action=RunScene&SceneNum="
        url += str(device)
        print url
        responce = self.plugin.HTTP_API.send(url)

    def Configure(self, device=1):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        panel.AddLine("Set Device", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())
        
#-----------------------------------------------------------------------------
class SetDimming(eg.ActionBase):
    name = "Set Light Level"
    description = "Sets a light to a percentage (%)."

    def __call__(self, device, percentage):
        print "Set " + str(device) + " to " + str(percentage)
        url = "/data_request?id=lu_action&DeviceNum="
        url += str(device)
        url += "&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget="
        url += str(percentage)
        responce = self.plugin.HTTP_API.send(url)

    def Configure(self, device=1, percentage=100):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        valueCtrl = panel.SpinNumCtrl(percentage, min=0, max=100)
        panel.AddLine("Set Device", deviceCtrl)
        panel.AddLine("Dim to", valueCtrl, "percent.")
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue(), valueCtrl.GetValue())
        
#-----------------------------------------------------------------------------
class SetSwitchPower(eg.ActionBase):
    name = "Set Binary Power"
    description = "Turn a switch on or off"
    functionList = ["Off", "On"]
    
    def __call__(self, device, value):
        print "Set " + str(device) + " to " + str(value)
        url = "/data_request?id=lu_action&DeviceNum="
        url += str(device)
        url += "&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue="
        url += str(value)
        responce = self.plugin.HTTP_API.send(url)

    def Configure(self, device=1, function="On"):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        functionCtrl = panel.Choice(1, self.functionList)
        panel.AddLine("Set Device", deviceCtrl)
        panel.AddLine("Value", functionCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue(), (functionCtrl.GetValue()))
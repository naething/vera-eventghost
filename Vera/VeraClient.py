import json
#import pprint

from VeraDevice import *

#pp = pprint.PrettyPrinter(indent=4)

#-----------------------------------------------------------------------------
# Vera Stuff
#-----------------------------------------------------------------------------

class VeraClient:
        
    #-----------------------------------------------------------------------------
    def __init__(self, ip, callback, debug_callback, dispatcher):
        self.ip          = ip
        self.dev         = {}
        self.dev_cat     = {}
        self.categories  = {}
        self.rooms       = {}
        self.base_url    = 'http://' + self.ip + ':3480/data_request?id=lu_sdata'
        self.callback    = callback
        self.debug_callback = debug_callback
        self.dispatcher  = dispatcher
        self.dispatcher.fetch(self.base_url, self.initial_load)

    #-----------------------------------------------------------------------------
    def BuildUrl(self, pairs):
        url = 'http://' + self.ip + ':3480/data_request?id=lu_action&'
        url = url + '&'.join(pairs)
        return url
        
    #-----------------------------------------------------------------------------
    def SwitchPower(self, devId, state):
        pairs = ['DeviceNum='+ str(devId),
                 'serviceId=urn:upnp-org:serviceId:SwitchPower1',
                 'action=SetTarget',
                 'newTargetValue='+str(state)]
        url = self.BuildUrl(pairs)
        #print url
        d = getPage(url)

    #-----------------------------------------------------------------------------
    def DimmableLight(self, devId, level):
        pairs = ['DeviceNum=' + str(devId),
                 'serviceId=urn:upnp-org:serviceId:SwitchPower1',
                 'action=SetTarget',
                 'newTargetValue=' + str(level)]
        url = self.BuildUrl(pairs)
        #print url
        d = getPage(url)

    #-----------------------------------------------------------------------------
    # we want to fetch just changed data since last load
    # this is specified by appending the previous dataversion
    # and time
    def create_new_url(self, data):
        # if for some reason the previous fetch didn't work this will throw a 
        # key exception, and then we just want to do a clean fetch
        try:
            return (self.base_url + "&loadtime="    + str(data['loadtime'])
                                  + "&dataversion=" + str(data['dataversion'])
                                  + "&timeout=60&minimumdelay=2000")
        except Exception: 
            self.debug_callback('Data Fetch Returned Bad Data, Performing Clean Load')
            self.dispatcher.fetch(self.base_url, self.initial_load)
   
    #-----------------------------------------------------------------------------
    def create_devices(self, data):
        
        dev_con = {}
        dev_con['Virtual']             = VeraVirtual
        dev_con['Sensor']              = VeraSensor
        dev_con['Humidity Sensor']     = VeraHumiditySensor
        dev_con['Dimmable Light']      = VeraDimmableLight
        dev_con['Switch']              = VeraSwitch
        dev_con['Camera']              = VeraCamera
        dev_con['Alarm Panel']         = VeraAlarmPanel
        dev_con['Temperature Sensor']  = VeraTempSensor
        dev_con["Alarm Partition"]     = VeraAlarmPartition
        dev_con["Door lock"]           = VeraDoorLock
        dev_con["Thermostat"]          = VeraThermostat
        
        # Fill in Categories
        for c in data['categories']:
            self.categories[c['id']] = c['name']

        # Hack for some 'virtual' devices with dev type == 0
        self.categories[0] = 'Virtual'

        # Fill in Rooms
        for r in data['rooms']:
            self.rooms[str(r['id'])] = r['name'];
        
        # Fill in Devices
        # Use proper constructor that is unique per Category
        for d in data['devices']:

            base = tuple(d.get(c, None) for c in VeraDevice.elements())            
            cat_idx = d['category']
            
            # Use Base Constructor for unknown devices
            if cat_idx not in self.categories:
                self.dev[str(d['id'])] = VeraDevice(*base)
                self.dev[str(d['id'])].callbacks.append(self.callback)
                
            # Known Categories
            elif self.categories[cat_idx] in dev_con.keys():                
                cat = self.categories[cat_idx]
                extentions = tuple(d.get(c, None) for c in dev_con[cat].elements())  
                self.dev[str(d['id'])] = dev_con[cat](base, *extentions)
                self.dev[str(d['id'])].callbacks.append(self.callback)
            
        #for d in self.dev:
        #    print str(self.dev[d].id) + str(self.dev[d])  
    
    #-----------------------------------------------------------------------------
    def debug_dump(self):
        names = tuple(self.dev[d].name for d in self.dev)
        return '<div>' + '</div><div>'.join(names) + '</div>'
    
    #-----------------------------------------------------------------------------
    def update(self, output):
        self.debug_callback('New Data Received from Vera')
        data = {}
        try:
            data = json.loads(output)
        except Exception:
            pass
        
        if 'devices' in data:
            for d in data['devices']:
                 key = str(d['id'])
                 if key in self.dev:
                     self.dev[key].update(d)

        self.call_next_url(data)
    
    #-----------------------------------------------------------------------------
    def call_next_url(self, data):
        try:
            new_url = self.create_new_url(data)
            self.dispatcher.fetch(new_url, self.update)
        except Exception:
            self.debug_callback('Data Fetch Failed, Performing Clean Load')
            self.dispatcher.fetch(self.base_url, self.initial_load)

    #-----------------------------------------------------------------------------
    def initial_load(self, output):
        try:
            data = json.loads(output)
            self.create_devices(data)
            self.debug_callback('Initial Data Received from Vera')
            self.call_next_url(data)
        except Exception:
            self.dispatcher.fetch(self.base_url, self.initial_load)
        

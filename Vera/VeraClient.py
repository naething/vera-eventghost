import json
#import pprint

from VeraDevice import *

#pp = pprint.PrettyPrinter(indent=4)

#-----------------------------------------------------------------------------
# Vera Stuff
#-----------------------------------------------------------------------------

class VeraClient:
        
    #-----------------------------------------------------------------------------
    def __init__(self, ip, callback, dispatcher):
        self.ip          = ip
        self.dev         = {}
        self.dev_cat     = {}
        self.categories  = {}
        self.base_url    = 'http://' + self.ip + ':3480/data_request?id=lu_sdata'
        self.callback    = callback
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
        return (self.base_url + "&loadtime="    + str(data['loadtime'])
                              + "&dataversion=" + str(data['dataversion'])
                              + "&timeout=60&minimumdelay=2000")
    
    #-----------------------------------------------------------------------------
    def fill_table(self, data, query, col, tag):
        for d in data[tag]:
            keys = tuple(d[c] for c in col)
            c.execute(query, keys)
    
    #-----------------------------------------------------------------------------
    def create_devices(self, data):
        
        dev_con = {}
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
        
        # Fill in Devices
        # Use proper constructor that is unique per Category
        for d in data['devices']:

            base = tuple(d.get(c, None) for c in VeraDevice.elements())            
            cat_idx = d['category']
            
            # Use Base Constructor for unknown devices
            if cat_idx not in self.categories:
                self.dev[str(d['id'])] = VeraDevice(self.callback, *base)
                
            # Known Categories
            elif self.categories[cat_idx] in dev_con.keys():                
                cat = self.categories[cat_idx]
                extentions = tuple(d.get(c, None) for c in dev_con[cat].elements())  
                self.dev[str(d['id'])] = dev_con[cat]((self.callback,) + base, *extentions)
            
        #for d in self.dev:
        #    print str(self.dev[d].id) + str(self.dev[d])  
    
    #-----------------------------------------------------------------------------
    def debug_dump(self):
        names = tuple(self.dev[d].name for d in self.dev)
        return '<div>' + '</div><div>'.join(names) + '</div>'
    
    #-----------------------------------------------------------------------------
    def update(self, output):
        data = json.loads(output)
        
        if 'devices' in data:
            for d in data['devices']:
                 key = str(d['id'])
                 self.dev[key].update(d)

        self.call_next_url(data)
    
    #-----------------------------------------------------------------------------
    def call_next_url(self, data):
        new_url = self.create_new_url(data)
        self.callback('NewData')
        self.dispatcher.fetch(new_url, self.update)
        
    #-----------------------------------------------------------------------------
    def initial_load(self, output):
        self.callback('InitialData')
        data = json.loads(output)
        self.create_devices(data)
        self.call_next_url(data)

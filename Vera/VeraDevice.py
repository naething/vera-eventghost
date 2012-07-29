import pprint

#-----------------------------------------------------------------------------
# Generic Objects:
class VeraDevice(object):

    def __init__ (self, callback, id, altid, category, name, parent, room, subcategory, status, comment):
         self.callback    = callback
         self.id          = id
         self.altid       = altid
         self.category    = category
         self.name        = name
         self.parent      = parent
         self.room        = room
         self.subcategory = subcategory
         self.status      = status
         self.comment     = comment
         
         # not passed in:
         self.watched     = []

    def __str__(self):
         return "%s" % self.name

    def update(self, d):
        changed = False
        
        # see if a monitored variable changed
        for watchedVar in self.watched:
             if (watchedVar in d.keys()) and d[watchedVar] != getattr(self,watchedVar):
                 changed = True
                     
        for k in d.keys():
            try:
                setattr(self, k, d[k])
            except AttributeError:
                print self.name + ' does not have an attribute ' + k

        if changed:
            self.callback(self)

    @staticmethod
    def elements():
        return ['id', 'altid', 'category', 'name', 'parent', 'room', 'subcategory', 'status', 'comment']

#----------------------------------------------------------------------------- 
# Category #2: Dimmable Lights       
class VeraDimmableLight(VeraDevice):

    def __init__ (self, base, level):
         super(VeraDimmableLight,self).__init__(*base)
         self.level   = level
         self.watched = ['status','level']
            
    def __str__(self):
        onOff = 'OFF' if self.status == '0' else 'ON'
        return(self.name + '.' + onOff + '.' + self.level)

    @staticmethod
    def elements():
        return ['level']

#-----------------------------------------------------------------------------
# Category #3: Switch     
class VeraSwitch(VeraDevice):

    def __init__ (self, base):
         super(VeraSwitch,self).__init__(*base)
         self.watched = ['status']
        
    def __str__(self):
        onOff = 'OFF' if self.status == '0' else 'ON'
        return(self.name + '.' + onOff)

    @staticmethod
    def elements():
        return []

#-----------------------------------------------------------------------------
# Category #4: Security Sensor
class VeraSensor(VeraDevice):

    def __init__ (self, base, lasttrip, tripped, armed):
         super(VeraSensor,self).__init__(*base)
         self.lasttrip = lasttrip
         self.tripped  = tripped
         self.armed    = armed
         self.watched  = ['armed', 'tripped']
        
    def __str__(self):
        trip = 'CLEAR' if self.tripped == '0' else 'TRIPPED'
        arm  = 'ARMED' if self.armed   == '1' else 'NOT_ARMED'
        return(self.name + '.' + arm + '.' + trip)
         
    @staticmethod
    def elements():
        return ['lasttrip', 'tripped', 'armed']

#-----------------------------------------------------------------------------
# Category #5: Thermostat       
class VeraThermostat(VeraDevice):

    def __init__ (self, base):
         super(VeraThermostat,self).__init__(*base)

    @staticmethod
    def elements():
        return []

#-----------------------------------------------------------------------------
# Category #6: Camera
class VeraCamera(VeraDevice):

    def __init__ (self, base, ip, url):
         super(VeraCamera,self).__init__(*base)
         self.ip  = ip
         self.url = url
         
    @staticmethod
    def elements():
        return ['ip', 'url']    
         
#----------------------------------------------------------------------------- 
# Category #7: Door Lock
class VeraDoorLock(VeraDevice):

    def __init__ (self, base, locked):
        super(VeraDoorLock,self).__init__(*base)  
        self.locked  = locked
        self.watched = ['locked']

    def __str__(self):
        lock = 'LOCKED' if self.locked == '1' else 'UNLOCKED'
        return(self.name + '.' + lock)
             
    @staticmethod
    def elements():
        return ['locked']
        

#----------------------------------------------------------------------------- 
# Category #8: Window Covering (dimmable light clone?)

  
#-----------------------------------------------------------------------------
# Category #16: Humidity Sensor    
class VeraHumiditySensor(VeraDevice):

    def __init__ (self, base, humidity):
         super(VeraHumiditySensor,self).__init__(*base)
         self.humidity  = humidity
         self.watched   = ['humidity'] 
        
    def __str__(self):
        return(self.name + '.' + str(self.humidity))
        
    @staticmethod
    def elements():
        return ['humidity']

#-----------------------------------------------------------------------------
# Category #17: Temperature Sensor        
class VeraTempSensor(VeraDevice):

    def __init__ (self, base, temperature):
         super(VeraTempSensor,self).__init__(*base)
         self.temperature = temperature
         self.watched     = ['temperature']
        
    def __str__(self):
        return(self.name + '.' + str(self.temperature))

    @staticmethod
    def elements():
        return ['temperature']

#-----------------------------------------------------------------------------   
# Category #21: Power Meter   

#-----------------------------------------------------------------------------   
# Category #22: Alarm Panel     
class VeraAlarmPanel(VeraDevice):

    def __init__ (self, base):
         super(VeraAlarmPanel,self).__init__(*base)
         
    @staticmethod
    def elements():
        return []
        

#-----------------------------------------------------------------------------
# Category #23: Alarm Partition 
class VeraAlarmPartition(VeraDevice):

    def __init__ (self, base):
        super(VeraAlarmPartition,self).__init__(*base)    
            
    @staticmethod
    def elements():
        return []


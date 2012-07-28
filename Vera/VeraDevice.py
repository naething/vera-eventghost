
#-----------------------------------------------------------------------------
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

    def __str__(self):
         return "%s" % self.name

    def update(self, d):
        for k in d.keys():
            try:
                setattr(self, k, d[k])
            except AttributeError:
                print self.name + ' does not have an attribute ' + k

    @staticmethod
    def elements():
        return ['id', 'altid', 'category', 'name', 'parent', 'room', 'subcategory', 'status', 'comment']

#-----------------------------------------------------------------------------
class VeraSensor(VeraDevice):

    def __init__ (self, base, lasttrip, tripped, armed):
         super(VeraSensor,self).__init__(*base)
         self.lasttrip = lasttrip
         self.tripped  = tripped
         self.armed    = armed
         
    @staticmethod
    def elements():
        return ['lasttrip', 'tripped', 'armed']

#-----------------------------------------------------------------------------        
class VeraHumiditySensor(VeraDevice):

    def __init__ (self, base, humidity):
         super(VeraHumiditySensor,self).__init__(*base)
         self.humidity  = humidity

    @staticmethod
    def elements():
        return ['humidity']

#-----------------------------------------------------------------------------        
class VeraDimmableLight(VeraDevice):

    def __init__ (self, base, level):
         super(VeraDimmableLight,self).__init__(*base)
         self.level  = level

    def update(self, d):
        update = False
        # if I was turned ON/OFF:
        if ('status' in d.keys()) and d['status'] != self.status:
             update = True
        # or my dimmed level changed:
        elif ('level' in d.keys()) and d['level'] != self.level:
             update = True
        super(VeraDimmableLight,self).update(d)
        if update:
            self.callback(self)
            
    def __str__(self):
        onOff = 'OFF' if self.status == '0' else 'ON'
        return(self.name + '.' + onOff + '.' + self.level)

    @staticmethod
    def elements():
        return ['level']

#-----------------------------------------------------------------------------        
class VeraSwitch(VeraDevice):

    def __init__ (self, base):
         super(VeraSwitch,self).__init__(*base)

    def update(self, d):
        update = False
        # if I was turned ON/OFF:
        if ('status' in d.keys()) and d['status'] != self.status:
             update = True
        super(VeraSwitch,self).update(d)
        if update:
            self.callback(self)
        
    def __str__(self):
        onOff = 'OFF' if self.status == '0' else 'ON'
        return(self.name + '.' + onOff)

    @staticmethod
    def elements():
        return []

#-----------------------------------------------------------------------------        
class VeraCamera(VeraDevice):

    def __init__ (self, base, ip, url):
         super(VeraCamera,self).__init__(*base)
         self.ip  = ip
         self.url = url
         
    @staticmethod
    def elements():
        return ['ip', 'url']    
         
#-----------------------------------------------------------------------------        
class VeraAlarmPanel(VeraDevice):

    def __init__ (self, base):
         super(VeraAlarmPanel,self).__init__(*base)
         
    @staticmethod
    def elements():
        return []
        
#-----------------------------------------------------------------------------        
class VeraTempSensor(VeraDevice):

    def __init__ (self, base):
         super(VeraTempSensor,self).__init__(*base)

    @staticmethod
    def elements():
        return []
        
#-----------------------------------------------------------------------------        
class VeraAlarmPartition(VeraDevice):

    def __init__ (self, base):
        super(VeraAlarmPartition,self).__init__(*base)    
            
    @staticmethod
    def elements():
        return []
                
#-----------------------------------------------------------------------------        
class VeraDoorLock(VeraDevice):

    def __init__ (self, base):
        super(VeraDoorLock,self).__init__(*base)  
              
    @staticmethod
    def elements():
        return []
         
#-----------------------------------------------------------------------------        
class VeraThermostat(VeraDevice):

    def __init__ (self, base):
         super(VeraThermostat,self).__init__(*base)

    @staticmethod
    def elements():
        return []
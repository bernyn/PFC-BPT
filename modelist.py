#SELECTOR MULTIPLE
import sys

from pylab import plotfile, show, gca
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from modenumerical import PopupUP
import matplotlib.cbook as cbook
import obd_sensors

RECOMMENDED_RPM = 2000

 
     
class ModeListPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeListPanel, self).__init__(*args, **kwargs)
        
         # Connection
        self.connection = None

        # Sensors 
        self.istart = 0
        self.sensors = []
        
        # Port 
        self.port = None
        
        self.rpm = 0
        self.speed = 0
        self.ecomode = False
        
        # Alarms
        self.alarm1mins, self.alarm1minval, self.alarm1Maxs,self.alarm1Maxval = [0]*4 
        self.alarm2mins, self.alarm2minval, self.alarm2Maxs,self.alarm2Maxval = [0]*4   
        self.alarm3mins, self.alarm3minval, self.alarm3Maxs,self.alarm3Maxval = [0]*4   
        self.alarm4mins, self.alarm4minval, self.alarm4Maxs,self.alarm4Maxval = [0]*4   
        self.alarm5mins, self.alarm5minval, self.alarm5Maxs,self.alarm5Maxval = [0]*4   
        self.alarm1t, self.alarm2t, self.alarm3t = "No alarm","No alarm","No alarm"
        self.alarm4t, self.alarm5t, self.alarm6t = "No alarm","No alarm","No alarm" 
        
        self.alarm1max,self.alarm2max,self.alarm3max,self.alarm4max,self.alarm5max,self.alarm6max, = [0]*6
        self.alarm1min,self.alarm2min,self.alarm3min,self.alarm4min,self.alarm5min,self.alarm6min, = [0]*6
        
    def showModeListPanel(self):           
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Sensor List Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer9.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 1 )
               
        print 'show passed port'
        print self.port
        #=======================================================================
        # panelList = wx.Panel( self, -1 )
        # leftPanel = wx.Panel(panelSettings, -1)
        #=======================================================================
        
        self.list = wx.ListCtrl(self.m_panel1, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list.InsertColumn(0, 'Name', width=140)
        self.list.InsertColumn(1, 'Value')
        self.list.InsertColumn(1, 'Units')
                         
  
        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        bSizer2.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        #define get and update values
        
        #call alerts
        #check eco mode
    
    def setEcoMode (self,eco):
        return self.ecomode 
         
    def setConnection(self, connection):
        self.connection = connection
    
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def setPort(self, port):
        self.port = port
    
    def getSensors(self):
        return self.sensors
    
    def getPort(self):
        return self.port

    def getSensorsToDisplay(self, istart):
        """
        Get at most 6 sensors to be display on screen.
        """
        sensors_display = []
        if istart<len(self.sensors):
            iend = istart + 6
            sensors_display = self.sensors[istart:iend]
        return sensors_display

    def ShowSensors(self):
        """
        Display the sensors.
        """
        print "showsensor  list"
        
        
        name =""
        value= ""
        unit= ""
        self.cfg = wx.Config('sensorsettings')
        num = self.list.GetItemCount()
       
        sensors = self.getSensorsToDisplay(self.istart)
        if self.cfg.Exists('Supported PIDs'):             
            print "creating list with conf"                
            for i,e in enumerate(obd_sensors.SENSORS):
                 
                if self.cfg.ReadBool(e.name)==True:
                    (name, value, unit) = self.port.sensor(i)
                    index = self.list.InsertStringItem(sys.maxint, e.name)
                    if type(value)==float:  
                        value = str("%.2f"%round(value, 3)) 
                    self.list.SetStringItem(index, 1, str(value))#e.value)
                    self.list.SetStringItem(index, 2, e.unit)      
        
        print "end creating list with conf"    
        itext = 0

        # Timer for update
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)
        self.timer.Start(2000)


    def refresh(self, event):
        print "refreshing sensors"
        sensors = self.getSensorsToDisplay(self.istart)   
        name =""
        value= ""
        unit= ""
        itext = 0
        for i,e in enumerate(obd_sensors.SENSORS): 
            if self.cfg.ReadBool(e.name)==True:
                (name, value, unit) = self.port.sensor(i)
                index = self.list.SetStringItem(sys.maxint, e.name)
                if type(value)==float:  
                    value = str("%.2f"%round(value, 3)) 
                self.list.SetStringItem(index, 1, str(value))#e.value)
                self.list.SetStringItem(index, 2, e.unit)  
                self.checkAlarm(name, value, unit)      
        
        print "finish refreshing list" 
                 
          
        
        #get speed    
        (name, value, unit) = self.port.sensor(13)
        self.speed =value            
       # print (name + str(value)+ unit)      
                 
        (name, value, unit) = self.port.sensor(12) 
        self.rpm = value
        #print (name + str(value)+ unit)
        
        if self.ecomode: 
            self.checkECOMode()
        
                
    def checkAlarm(self,name, value, unit):
        if name == self.alarm1t: 
            if self.alarm1mins == 1 and  float(value) < self.alarm1minval and self.alarm1min< 3:
                wx.MessageBox('Alarm 1 Min.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 1 Min ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm1min += 1          
            if self.alarm1Maxs == 1 and  float(value) > self.alarm1Maxval and self.alarm1max < 3:
                wx.MessageBox('Alarm 1 Max.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 1 Max ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm1max += 1
        if name == self.alarm2t: 
            if self.alarm2mins == 1 and  float(value) < self.alarm2minval and self.alarm2min< 3:
                wx.MessageBox('Alarm 2 Min.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 2 Min ON', wx.OK | wx.ICON_EXCLAMATION)                
                self.alarm2min += 1
            if self.alarm2Maxs == 1 and  float(value) > self.alarm2Maxval and self.alarm2max < 3:
                wx.MessageBox('Alarm 2 Max.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 2 Max ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm2max += 1
        if name == self.alarm3t: 
            if self.alarm3mins == 1 and  float(value) < self.alarm3minval and self.alarm3min< 3:
                wx.MessageBox('Alarm 3 Min.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 3 Min ON', wx.OK | wx.ICON_EXCLAMATION)                
                self.alarm3min += 1
            if self.alarm3Maxs == 1 and  float(value) > self.alarm3Maxval and self.alarm3max < 3:
                wx.MessageBox('Alarm 3 Max.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 3 Max ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm3max += 1
        if name == self.alarm4t: 
            if self.alarm4mins == 1 and  float(value) < self.alarm4minval and self.alarm4min< 3:
                wx.MessageBox('Alarm 4 Min.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 4 Min ON', wx.OK | wx.ICON_EXCLAMATION)                
                self.alarm4min += 1
            if self.alarm4Maxs == 1 and  float(value) > self.alarm4Maxval and self.alarm4max < 3:
                wx.MessageBox('Alarm 4 Max.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 4 Max ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm4max += 1
        if name == self.alarm5t: 
            if self.alarm5mins == 1 and  float(value) < self.alarm5minval and self.alarm5min< 3:
                wx.MessageBox('Alarm 5 Min.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 5 Min ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm5min += 1
            if self.alarm5Maxs == 1 and  float(value) > self.alarm5Maxval and self.alarm5max < 3:
                wx.MessageBox('Alarm 5 Max.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 5 Max ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm5max += 1
        if name == self.alarm6t: 
            if self.alarm6mins == 1 and  float(value) < self.alarm6minval and self.alarm6min< 3:
                wx.MessageBox('Alarm 6 Min.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 6 Min ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm6min += 1                 
            if self.alarm6Maxs == 1 and  float(value) > self.alarm6Maxval and self.alarm6max < 3:
                wx.MessageBox('Alarm 6 Max.: ' + name + " flagged  :"+ str(value)+ " "+ str(unit), 'Alarm 6 Max ON', wx.OK | wx.ICON_EXCLAMATION)
                self.alarm6max += 1
        if self.alarm1min>= 3:
                self.alarm1min= 0
        if self.alarm2min>= 3:
                self.alarm2min= 0
        if self.alarm3min>= 3:
                self.alarm3min= 0
        if self.alarm4min>= 3:
                self.alarm4min= 0
        if self.alarm5min>= 3:
                self.alarm5min= 0
        if self.alarm6min>= 3:
                self.alarm6min= 0
        if self.alarm1max>= 3:
                self.alarm1max= 0
        if self.alarm2max>= 3:
                self.alarm2max= 0
        if self.alarm3max>= 3:
                self.alarm3max= 0
        if self.alarm4max>= 3:
                self.alarm4max= 0
        if self.alarm5max>= 3:
                self.alarm5max= 0
        if self.alarm6max>= 3:
                self.alarm6max= 0   
                
    def getRecords(self, event):
        
       self.cfg = wx.Config('recordsettings')
       self.num = self.list.GetItemCount()
       self.sensorlist = []
       for i in range(self.num):
            self.sensorlist.append(False)
       if self.cfg.Exists('Supported PIDs'):                     
            for i in range(self.num):
                self.list.CheckItem(i,self.cfg.ReadBool(self.list.GetItemText(i)))  
                                        
       else:
            for i in range(self.num):
                self.list.CheckItem(i,False)
    
    def getAlarms(self):
    
        self.cfg = wx.Config('alarmsettings')
        if self.cfg.Exists('alarm1minstatus'):  
            self.alarm1mins, self.alarm1minval, self.alarm1Maxs,self.alarm1Maxval = self.cfg.ReadInt('alarm1minstatus'), self.cfg.ReadInt('alarm1minvalue'),self.cfg.ReadInt('alarm1Maxstatus'), self.cfg.ReadInt('alarm1Maxvalue')    
            self.alarm2mins, self.alarm2minval, self.alarm2Maxs,self.alarm2Maxval = self.cfg.ReadInt('alarm2minstatus'), self.cfg.ReadInt('alarm2minvalue'),self.cfg.ReadInt('alarm2Maxstatus'), self.cfg.ReadInt('alarm2Maxvalue')
            self.alarm3mins, self.alarm3minval, self.alarm3Maxs,self.alarm3Maxval = self.cfg.ReadInt('alarm3minstatus'), self.cfg.ReadInt('alarm3minvalue'),self.cfg.ReadInt('alarm3Maxstatus'), self.cfg.ReadInt('alarm3Maxvalue')
            self.alarm4mins, self.alarm4minval, self.alarm4Maxs,self.alarm4Maxval = self.cfg.ReadInt('alarm4minstatus'), self.cfg.ReadInt('alarm4minvalue'),self.cfg.ReadInt('alarm4Maxstatus'), self.cfg.ReadInt('alarm4Maxvalue')
            self.alarm5mins, self.alarm5minval, self.alarm5Maxs,self.alarm5Maxval = self.cfg.ReadInt('alarm5minstatus'), self.cfg.ReadInt('alarm5minvalue'),self.cfg.ReadInt('alarm5Maxstatus'), self.cfg.ReadInt('alarm5Maxvalue')
            self.alarm1t, self.alarm2t, self.alarm3t, self.alarm4t, self.alarm5t = self.cfg.Read('alarm1'), self.cfg.Read('alarm2'), self.cfg.Read('alarm3'), self.cfg.Read('alarm4'), self.cfg.Read('alarm5')
        else:
             
            self.cfg.Write("alarm1","Vehicle Speed")
            self.cfg.WriteInt("alarm1minstatus", 1)
            self.cfg.WriteInt("alarm1minvalue", 10)
            self.cfg.WriteInt("alarm1Maxstatus", 1)
            self.cfg.WriteInt("alarm1Maxvalue", 90)
            self.cfg.Write("alarm2","No alarm")
            self.cfg.WriteInt("alarm2minstatus", 0)
            self.cfg.WriteInt("alarm2minvalue", 0)
            self.cfg.WriteInt("alarm2Maxstatus", 0)
            self.cfg.WriteInt("alarm2Maxvalue", 0)    
            self.cfg.Write("alarm3","No alarm")
            self.cfg.WriteInt("alarm3minstatus", 0)
            self.cfg.WriteInt("alarm3minvalue", 0)
            self.cfg.WriteInt("alarm3Maxstatus", 0)
            self.cfg.WriteInt("alarm3Maxvalue", 0)
            self.cfg.Write("alarm4","No alarm")
            self.cfg.WriteInt("alarm4minstatus", 0)
            self.cfg.WriteInt("alarm4minvalue", 0)
            self.cfg.WriteInt("alarm4Maxstatus", 0)
            self.cfg.WriteInt("alarm4Maxvalue", 0)
            self.cfg.Write("alarm5","No alarm")
            self.cfg.WriteInt("alarm5minstatus", 0)
            self.cfg.WriteInt("alarm5minvalue", 0)
            self.cfg.WriteInt("alarm5Maxstatus", 0)
            self.cfg.WriteInt("alarm5Maxvalue", 0)
   
    def checkECOMode(self, event):
        print "on check eco"
        gear= self.get_gear(self.speed,self.rpm)
        print str(gear)
        if gear < 5 and self.rpm < RECOMMENDED_RPM:
            self.winup = PopupUP(self.GetTopLevelParent(),  wx.SIMPLE_BORDER)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (300,0) )
            sz =  btn.GetSize()
            self.winup.Position(pos, (0, sz[1]))
            self.winup.Show(True)
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.onCloseUp, self.timer)
            self.timer.Start(3000)
            
    
    def get_gear(self, speed, rpm):
        #Data for Dacia Logan, from http://renault.cw/logan_specifications.php
        gear_ratios = [3.72, 2.05, 1.32, 0.97, 0.76]
        if speed == 0 or speed == "": return 0
        if rpm == 0 or rpm == "":     return 0

        rps = rpm/60
        kmps = (speed*1000)/3600
        
        first_gear = 3.72  
        final_gear_ratio  = 4.3
        
        #for 185/65R15 tyres
        tyre_circ = 1.95 #tyres 24.5'' *2.54cm*pi/100 in meters

        actual_gear_ratio = (rps*tyre_circ)/(kmps*first_gear*final_gear_ratio)
        
        #print current_gear_ratio
        gear = min((abs(actual_gear_ratio - i), i) for i in gear_ratios)[1] 
        return gear
    

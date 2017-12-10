#SELECTOR MULTIPLE
import sys

from pylab import plotfile, show, gca
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from modenumerical import PopupUP
import matplotlib.cbook as cbook
import wx.lib.agw.pybusyinfo as PBI
from datetime import datetime
import time
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
    
    def setRecordFile(self, record):
        self.record_file = record
    
    def getRecordFile(self):
        return self.record_file

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
            self.header = "Date; Time"
            for i,e in enumerate(obd_sensors.SENSORS):
                 
                if self.cfg.ReadBool(e.name)==True:
                    (name, value, unit) = self.port.sensor(i)
                    index = self.list.InsertStringItem(sys.maxint, e.name)
                    if type(value)==float:  
                        value = str("%.2f"%round(value, 3)) 
                    self.list.SetStringItem(index, 1, str(value))#e.value)
                    self.list.SetStringItem(index, 2, e.unit)      
                    self.header += (name+ ";")
            self.header += ";"+ "\n"
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
        line=""
        date= time.strftime("%x") + ";" + time.strftime("%X")+ ";" 
        line=date
        itext = 0
        self.list.DeleteAllItems()
        for i,e in enumerate(obd_sensors.SENSORS): 
            if self.cfg.ReadBool(e.name)==True:
                (name, value, unit) = self.port.sensor(i)
                index = self.list.InsertStringItem(sys.maxint, e.name)
                if type(value)==float:  
                    value = str("%.2f"%round(value, 3)) 
                self.list.SetStringItem(index, 1, str(value))#e.value)
                self.list.SetStringItem(index, 2, e.unit)  
                self.checkAlarm(name, value, unit)      
                line += date + name + ";" + str(value) + ";" + str(unit) + "\n"
        
        self.valuetoggle= False
        if self.cfg.Exists('RecordMode'):
            self.valuetoggle= self.cfg.ReadBool('RecordMode') 
            if self.valuetoggle:
                
                self.recordfile = self.getRecordFile()
                print ("Line in " + self.recordfile)
                print(line)
                print "finish refreshing list" 
                self.write_record(self.recordfile, line)          
        print(line)  
        
        #get speed    
        (name, value, unit) = self.port.sensor(13)
        self.speed =value            
       # print (name + str(value)+ unit)      
                 
        (name, value, unit) = self.port.sensor(12) 
        self.rpm = value
        #print (name + str(value)+ unit)
        
        if self.ecomode: 
            self.checkECOMode()
        
    def write_record(self,file_record,line):   
        f = open(file_record, 'w')
        f.write(line) #Give your csv text here.
        f.close()            

    def checkAlarm(self,name, value, unit):
        if name == self.alarm1t: 
            if self.alarm1mins == 1 and  float(value) < self.alarm1minval:
                d = showalarm("Alarm 1 Min.:", name, str(value), str(unit))
                time.sleep(1.5)
            if self.alarm1Maxs == 1 and  float(value) > self.alarm1Maxval:
                d = showalarm("Alarm 1 Max.:", name, str(value), str(unit))
                time.sleep(1.5)
        if name == self.alarm2t: 
            if self.alarm2mins == 1 and  float(value) < self.alarm2minval:
                d = showalarm("Alarm 2 Min.:", name, str(value), str(unit))
                time.sleep(1.5)
            if self.alarm2Maxs == 1 and  float(value) > self.alarm2Maxval:
                d = showalarm("Alarm 2 Max.:", name, str(value), str(unit))
                time.sleep(1.5)
        if name == self.alarm3t: 
            if self.alarm3mins == 1 and  float(value) < self.alarm3minval:
                d = showalarm("Alarm 3 Min.:", name, str(value), str(unit))
                time.sleep(1.5)
            if self.alarm3Maxs == 1 and  float(value) > self.alarm3Maxval:
                d = showalarm("Alarm 3 Max.:", name, str(value), str(unit))
                time.sleep(1.5)
        if name == self.alarm4t: 
            if self.alarm4mins == 1 and  float(value) < self.alarm4minval:
                d = showalarm("Alarm 4 Min.:", name, str(value), str(unit))
                time.sleep(1.5)
            if self.alarm4Maxs == 1 and  float(value) > self.alarm4Maxval:
                d = showalarm("Alarm 4 Max.:", name, str(value), str(unit))
                time.sleep(1.5)
        if name == self.alarm5t: 
            if self.alarm5mins == 1 and  float(value) < self.alarm5minval:
                d = showalarm("Alarm 5 Min.:", name, str(value), str(unit))
                time.sleep(1.5)
            if self.alarm5Maxs == 1 and  float(value) > self.alarm5Maxval:
                d = showalarm("Alarm 5 Max.:", name, str(value), str(unit))
                time.sleep(1.5)

    def getRecords(self):
        
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
        
       self.valuetoggle= False
       if self.cfg.Exists('RecordMode'):
           self.valuetoggle= self.cfg.ReadBool('RecordMode') 
        
        
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

def showalarm(alarm, name, value, unit):
    msg = name + str(value)+ " "+ str(unit)
    title = "Alarm "+ alarm + " flagged:"
    d = PBI.PyBusyInfo(msg, title=title)
    return d    

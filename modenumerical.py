#SELECTOR MULTIPLE
import sys

from pylab import plotfile, show, gca
#from init import PFCFrame
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

import matplotlib.cbook as cbook
import obd_sensors

from datetime import datetime
import time

RECOMMENDED_RPM = 2000

########################################################################
class PopupUP(wx.PopupWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, style):
        """Constructor"""
        wx.PopupWindow.__init__(self, parent,style )

        panel = wx.Panel(self)
        self.panel = panel
              
        pngup = wx.Bitmap(u"./icons/Actions-arrow-up-icon.png", wx.BITMAP_TYPE_ANY ) 
        wx.StaticBitmap(self, -1, pngup, (-1, -1), (pngup.GetWidth(), pngup.GetHeight()))
        
        wx.CallAfter(self.Refresh)    
 
########################################################################

class PopupAlarm(wx.PopupWindow):
    #----------------------------------------------------------------------
    def __init__(self, parent, style):
        """Constructor"""
        wx.PopupWindow.__init__(self, parent,style )

        panel = wx.Panel(self)
        self.panel = panel
              
        pngup = wx.Bitmap(u"./icons/alarm_ico.png", wx.BITMAP_TYPE_ANY ) 
        wx.StaticBitmap(self, -1, pngup, (-1, -1), (pngup.GetWidth(), pngup.GetHeight()))
        
        wx.CallAfter(self.Refresh)    
 
########################################################################

       
        
########################################################################
class ModeNumericalPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeNumericalPanel, self).__init__(*args, **kwargs)

        # Connection
        self.connection = None

        # Sensors 
        self.istart = 0
        self.sensors = []
        
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
        
        # Port 
        self.port = None

        # List to hold children widgets
        self.boxes = []
        self.texts = []

        # Create an accelerator table
        lid = wx.NewId()
        cid = wx.NewId()
        rid = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onCtrlC, id=cid)
        self.Bind(wx.EVT_MENU, self.onLeft, id=lid)
        self.Bind(wx.EVT_MENU, self.onRight, id=rid)
        self.accel_tbl = wx.AcceleratorTable([ 
                (wx.ACCEL_CTRL, ord('C'), cid), 
                (wx.ACCEL_NORMAL, wx.WXK_LEFT, lid), 
                (wx.ACCEL_NORMAL, wx.WXK_RIGHT, rid), 
                ])
        self.SetAcceleratorTable(self.accel_tbl)

        # Handle events for mouse clicks
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeft)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRight)
              

    def showModeNumericalPanel(self):           
        
        #self.value = 2.88
        print 'show passed port'
        print self.port
        self.ShowSensors()
        
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
    
    def setEcoMode (self,eco):
        return self.ecomode

    def getSensorsToDisplay(self, istart):
        """
        Get at most 1 sensor to be displayed on screen.
        """
        sensors_display = []
        if istart<len(self.sensors):
            iend = istart + 1
            sensors_display = self.sensors[istart:iend]
        return sensors_display

    def ShowSensors(self):
        """
        Display the sensors.
        """
        print 'showsensors'
        print self.port
        sensors = self.getSensorsToDisplay(self.istart)
        name =""
        value= ""
        unit= ""
        # Destroy previous widgets
        for b in self.boxes: b.Destroy()
 #       for t in self.texts: t.Destroy()
  #      self.boxes = []
   #     self.texts = []

        boxSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.panelbox = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, (250,200), wx.TAB_TRAVERSAL )
        staticBox = wx.StaticBoxSizer( wx.StaticBox( self.panelbox, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
        
        # Create a box for each sensor
        for index, sensor in sensors:
            print 'creating boxes'
            (name, value, unit) = self.port.sensor(index)
            box = wx.StaticBox( self, -1, "Sensor" )
            self.boxes.append(box)
            self.boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            print ('Value= ' + str(value))
            print ('name=' + str(name))
            print ('unit=' + str(unit))
            
            # Text for sensor value 
            if type(value)==float:  
                value = str("%.2f"%round(value, 3))                    
    		print 'sensor in box'
            
            
            self.sensorData = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, str(value), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sensorData.Wrap( -1 )
            self.sensorData.SetFont( wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)) 
            staticBox.Add( self.sensorData, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            
            self.sensorUnit = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, str(unit), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sensorUnit.Wrap( -1 )
            staticBox.Add( self.sensorUnit, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            
            self.sensorName = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sensorName.Wrap( -1 )
            staticBox.Add( self.sensorName, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            
            
            
            
        self.panelbox.SetSizer( staticBox )
        self.panelbox.Layout()
        staticBox.Fit( self.panelbox )
        boxSizer.Add( self.panelbox, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( boxSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )      
           
        #get Alarms values
        self.getAlarms()
        
        #check Alarm status
        self.checkAlarm(name, value, unit)    
        
        # Timer for update
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)
        self.timer.Start(1000)


    def refresh(self, event):
        sensors = self.getSensorsToDisplay(self.istart)   
        #self.value = self.value +10
        itext = 0
        for index, sensor in sensors:
            (name, value, unit) = self.port.sensor(index)
            
            if type(value)==float:  
                value = str("%.2f"%round(value, 3))  
                print ('Value Refresh= ' + str(value))
                self.sensorData.SetLabel(str(value))
            else:
                self.sensorData.SetLabel(str(value))    
            
            self.sensorName.SetLabel(str(name))
            self.sensorUnit.SetLabel(str(unit))
            
            if itext<len(self.texts):
                self.texts[itext*2].SetLabel(str(value))
            
            if name == "Engine RPM" : self.rpm = value
            
            if name == "Vehicle Speed" : self.speed =value
            self.checkAlarm(name, value, unit)       
         
            itext += 1
        
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
    

    
    
    def onCloseUp(self, event):
        if self.winup.IsShown():
            self.winup.Show(False)
        self.timer.Stop()            
    
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
    
    def onCtrlC(self, event):
        self.GetParent().Close()

    def onLeft(self, event):
        """
        Get data from 1 previous sensor in the list.
        """
        print 'onleft'
        #self.value = self.value -1
        istart = self.istart + 1
        if istart<len(self.sensors):
            self.istart = istart
            self.ShowSensors()
        else: 
            istart = self.istart - 31 
            self.istart = istart 
            self.ShowSensors() 
                
    def onRight(self, event):
        """
        Get data from 1 next sensor in the list.
        """
        #self.value = self.value +1
        print 'onright'
        istart = self.istart + 1
        if istart<len(self.sensors):
            self.istart = istart
            self.ShowSensors()
        else: 
            istart = self.istart - 31 
            self.istart = istart 
            self.ShowSensors()
    
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
            self.cfg.Write("alarm1","No alarm")
            self.cfg.WriteInt("alarm1minstatus", 0)
            self.cfg.WriteInt("alarm1minvalue", 0)
            self.cfg.WriteInt("alarm1Maxstatus", 0)
            self.cfg.WriteInt("alarm1Maxvalue", 0)
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
        print "on test"
        gear= self.get_gear(self.speed,self.rpm)
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
        


#SELECTOR MULTIPLE
import sys
from threading import Thread

from pylab import plotfile, show, gca
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

import matplotlib.cbook as cbook
from obd_capture import OBD_Capture
from obd_sensors import *
from obd_sensors import SENSORS


class ModeNumericalPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeNumericalPanel, self).__init__(*args, **kwargs)

    def showModeNumericalPanel(self):           
        
        #self.value = 2.88
        # Connection
        self.c = OBD_Capture()
                
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
        
        # Connection
        self.connection = None

        # Sensors 
        self.istart = 0
        self.sensors = self.c.getSupportedSensorList()
        print 'c.getsupported sensor'
        print self.sensors
        
        
        # Port 
        self.port = self.c.is_connected()

        # List to hold children widgets
        self.boxes = []
        self.texts = []


    def setConnection(self, connection):
        self.connection = connection
    
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def setPort(self, port):
        self.port = port

    def getSensorsToDisplay(self, istart):
        """
        Get at most 1 sensor to be displayed on screen.
        """
        sensors_display = []
        if istart<len(self.sensors):
            iend = istart + 1
            sensors_display = self.sensors[istart:iend]
        print 'in sensors sensors_display'
        print sensors_display
        return sensors_display

    def ShowSensors(self):
        """
        Display the sensors.
        """
        print 'showsensors'
        sensors = self.getSensorsToDisplay(self.istart)
        print sensors

        # Destroy previous widgets
        for b in self.boxes: b.Destroy()
        for t in self.texts: t.Destroy()
        self.boxes = []
        self.texts = []

        boxSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.panelbox = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        staticBox = wx.StaticBoxSizer( wx.StaticBox( self.panelbox, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
        
        
        

        # Create a box for each sensor
        for index, sensor in sensors:
            print 'creating boxes'
            (name, value, unit) = self.port.sensor(index)

            box = wx.StaticBox( self, -1, "Special Text Ctrl" )
            self.boxes.append(box)
            self.boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)

            
            # Text for sensor value 
            if type(value)==float:  
                value = str("%.2f"%round(value, 3))                    
            self.sensorData = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, str(value), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sensorData.Wrap( -1 )
            self.sensorData.SetFont( wx.Font( 18, 74, 90, 90, False, "Arial" ) )
            
            staticBox.Add( self.sensorData, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            
            self.sensorName = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sensorName.Wrap( -1 )
            staticBox.Add( self.sensorName, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            

        # Add invisible boxes if necessary
#===============================================================================
#         nsensors = len(sensors)
#         
#         for i in range(1-nsensors):
#             print 'invisible box'
#             box = wx.StaticBox( self, -1, "Text" )
#             self.boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#             self.boxes.append(box)
# 
#             self.sensorData = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, str(value), wx.DefaultPosition, wx.DefaultSize, 0 )
#             self.sensorData.Wrap( -1 )
#             self.sensorData.SetFont( wx.Font( 18, 74, 90, 90, False, "Arial" ) )
#             
#             staticBox.Add( self.sensorData, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
#             
#             self.sensorName = wx.StaticText( staticBox.GetStaticBox(), wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0 )
#             self.sensorName.Wrap( -1 )
#             staticBox.Add( self.sensorName, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
#===============================================================================
        
        
        self.panelbox.SetSizer( staticBox )
        self.panelbox.Layout()
        staticBox.Fit( self.panelbox )
        boxSizer.Add( self.panelbox, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( boxSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )      
           
       
 
        # Timer for update
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)
        self.timer.Start(1000)


    def refresh(self, event):
        sensors = self.getSensorsToDisplay(self.istart)   
        #self.value = self.value +10
        itext = 0
        for index, sensor in sensors:
            print 'refresh sensor'
            (name, value, unit) = self.port.sensor(index)
            if type(value)==float:  
                value = str("%.2f"%round(value, 3))                    

            if itext<len(self.texts):
                self.texts[itext*2].SetLabel(str(value))
            
            itext += 1


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

   


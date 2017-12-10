# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from _sqlite3 import connect
from datetime import datetime
import os
from threading import Thread
import time

import wx
import wx.animate
import wx.xrc

from DTCs import DTCsPanel
from modegraphical import ModeGraphicalPanel
from modelist import ModeListPanel
from modenumerical import ModeNumericalPanel
from obd_capture import OBD_Capture
from obd_sensors import *
from obd_sensors import SENSORS
import obd_sensors
from records import RecordsPanel
from settinglarm import SettingAlarmsPanel
from settingrecords import SettingRecordPanel
from settingsensor import SettitingSensorPanel
from settingserial import SettingSerialPanel


PANEL_MAIN = "00"

PANEL_SETTINGS_SENSORS = "01"
PANEL_SETTINGS_RECORDS = "02"
PANEL_SETTINGS_ALARM = "03"
PANEL_SETTINGS_SERIAL = "04"

PANEL_RECORDS = "05"
PANEL_DTC = "06"

PANEL_MODE_GRAPHICAL = "07"
PANEL_MODE_NUMERICAL ="08"
PANEL_MODE_LIST = "09"


def obd_connect(o):
    o.connect()
    
#def obd_record(o):
 #   o.record()

class OBDConnection(object):
    """
    Class for OBD connection. Use a thread for connection.
    """
    
    def __init__(self):
        self.c = OBD_Capture()

    def get_capture(self):
        return self.c

    def connect(self):
        self.t = Thread(target=obd_connect, args=(self.c,))
        self.t.start()
    
   # def record(self):
    #    self.tcapt=Thread(target=obd_record, args=(self.c,))
     #   self.tcapt.start()

    def is_connected(self):
        return self.c.is_connected()

    def get_output(self):
        if self.c and self.c.is_connected():
            print "get output"
            print self.c.record()
            return self.c.record()
        return ""

    def get_port(self):
        return self.c.is_connected()

    def get_port_name(self):
        if self.c:
            port = self.c.is_connected()
            if port:
                try:
                    return port.port.name
                except:
                    pass
        return None
    
    def get_sensors(self):
        sensors = []
        if self.c:
            sensors = self.c.getSupportedSensorList()
        print "get sensors"
        print sensors
        return sensors

    def get_supported_sensor_list(self):
        supported_sensor_list=[]
        
    def get_dtc(self):
        dtcs = []
        if self.c:
            dtcs = self.c.capture_dtc()
        return dtcs
    
    def get_dtc_f(self):
        dtcfs = []
        if self.c:
            dtcfs = self.c.capture_dtc_f()
        return dtcfs
    
    def clear_dtc(self):
        result = []
        if self.c:
            result = self.c.clear_dtc()
        return result
        
    #===========================================================================
    # def record_data(self):
    #     text = ""
    #     supported_sensor_list= self.get_supported_sensor_list()
    #            
    #     if(self.port is None):
    #         return None
    #           
    #     line=""
    #     line = time.strftime("%x") + ";" + time.strftime("%X")+ ";"
    #   
    #     for supportedSensor in supported_sensor_list:
    #         sensorIndex = supportedSensor[0]
    #         (name, value, unit) = self.port.sensor(sensorIndex)
    #         line += name + ";" + str(value) + ";" + str(unit) + "\n"
    #     self.write_record(line)
    #     return line
    #===========================================================================

    def createRecordFile(self):
        self.path= os.path.dirname(__file__)
        self.record_path = os.path.join(self.path, 'recrods/')
        self.filedate = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')       
        self.record_file = "records-" +self.filedate +".csv"
        f = open(self.record_file, 'w')
        f.close()

        if not os.path.isdir(self.record_path):
            os.makedirs(self.record_path)
    
    def get_record_file(self):
        return self.record_file    
            
    
    def write_record(self,file_record,line):   
        f = open(file_record, 'w')
        f.write(line) #Give your csv text here.
        f.close()
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------

class OBDStaticBox(wx.StaticBox):
    """
    OBD StaticBox.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.StaticBox.__init__(self, *args, **kwargs)

   

#-------------------------------------------------------------------------------

###########################################################################
## Class frameInit                    START
###########################################################################

class OBDText(wx.TextCtrl):
    """
    Text display while loading OBD application.
    """

    def __init__(self, parent):
        """
        Constructor.
        """
        style = wx.TE_READONLY | wx.TE_MULTILINE
        wx.TextCtrl.__init__(self, parent, style=style)

        #self.SetBackgroundColour('#21211f')
        #self.SetForegroundColour(wx.WHITE)  

        font = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL, faceName="Monaco")
        self.SetFont(font)

    def AddText(self, text):
        self.AppendText(text)
        


class OBDLoadingPanel(wx.Panel):
    """
    Main panel for OBD application. 

    Show loading screen. Handle event from mouse/keyboard.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        super(OBDLoadingPanel, self).__init__(*args, **kwargs)

        # Background image
        self.SetBackgroundColour("black")

        # Connection
        self.c = None

        # Sensors list
        self.sensors = []

        # Port
        self.port = None

    def getConnection(self):
        return self.c
        
        
    def showLoadingScreen(self):
        """
        Display the loading screen.
        """
                
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        gif_fname = u"./icons/loading 80.gif" 
        self.gif = wx.animate.GIFAnimationCtrl(self, wx.ID_ANY, gif_fname)
        self.gif.GetPlayer().UseBackgroundColour(True)
        self.gif.Play()
        boxSizer.Add(self.gif, 1,  wx.EXPAND |  wx.ALIGN_CENTER, 0)
        self.textCtrl = OBDText(self)
        boxSizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(boxSizer)
        font3 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL, faceName="Monaco")
        self.textCtrl.SetFont(font3)
        self.textCtrl.AddText(" PFC Bernardo Plaza Trillo\n")     
        self.textCtrl.AddText(" Opening interface (serial port)\n")     
        self.textCtrl.AddText(" Trying to connect...\n")
        
        self.timer0 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.connect, self.timer0)
        self.timer0.Start(1000)
        
        self.Centre( wx.BOTH )
        self.Show(True)
        
        
        self.Layout() 
    
    def connect(self, event):
        if self.timer0:
            self.timer0.Stop()

        # Connection
        self.c = OBDConnection()
        self.c.connect()
        connected = False
        start_time = datetime.now()
        print(start_time)
        self.textCtrl.AddText(" Trying to connect ..." + time.asctime())
        self.gif.Play()
        while not connected:
            connected = self.c.is_connected()
            #self.textCtrl.Clear()
        
            
            if connected: 
                break


        if not connected:
            self.textCtrl.AddText(" Not connected\n")
            return False
        else:
            #self.textCtrl.Clear()
            print(" Connected\n")
            port_name = self.c.get_port_name()
            if port_name:
                self.textCtrl.AddText(" Failed Connection: " + port_name +"\n")
                self.textCtrl.AddText(" Please hold alt & esc to view terminal.")
            self.textCtrl.AddText(str(self.c.get_output()))
            #print str(self.c.get_output()) 
            self.sensors = self.c.get_sensors()
            self.port = self.c.get_port()
            print 'sensor and port'
            print self.sensors
            print self.port
            self.GetParent().update(None)


    def getSensors(self):
	print ('getsensors')
        return self.sensors
    
    def getPort(self):
        return self.port

    #===========================================================================
    # def getSupportedSensorList(self):
    #     return self.supported_list
    # 
    # def getUnSupportedSensorList(self):
    #     return self.unsupported_list
    #===========================================================================

    def getClass(self):
        return self.c
    
    def onCtrlC(self, event):
        self.GetParent().Close()



#___________________________________________________________________________
   
class PFCFrame(wx.Frame):
    """
    OBD frame.
    """

    def __init__(self):
        """
        Constructor.
        """        
        wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = u"Bernardo Plaza Project", pos = (0,0), size = wx.Size( 320,240 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.Size( 320,240 ), wx.Size( 320,240 ) )
        self.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        self.statusbar = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )       
        self.statusbar.SetStatusWidths([-1, 80])
        self.statusbar.SetFont( wx.Font( 6, 74, 90, 91, False, "Calibri Light" ) )
        statusbar_fields = ['Ready','Time']
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.timer = wx.Timer(self)   
        self.timer.Start(1000)
        self.timerDTC = wx.Timer(self, id=2)
        
        self.connection = None
        self.sensors = []
        self.port = None
        self.ecomode = False
        
        
        self.menubar = wx.MenuBar( 0 )
        self.menuFile = wx.Menu()
        self.menuSettings = wx.Menu()
        self.menuSensors = wx.MenuItem( self.menuSettings, wx.ID_ANY, u"Sensors", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSensors.SetBitmap( wx.Bitmap( u"./icons/Industry-Electrical-Sensor-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuSettings.AppendItem( self.menuSensors )
        
        self.menuRecordsSettings = wx.MenuItem( self.menuSettings, wx.ID_ANY, u"Records", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuRecordsSettings.SetBitmap( wx.Bitmap( u"./icons/Actions-office-chart-line-stacked-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuSettings.AppendItem( self.menuRecordsSettings )
        
        self.menuAlarm = wx.MenuItem( self.menuSettings, wx.ID_ANY, u"Alarms", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuAlarm.SetBitmap( wx.Bitmap( u"./icons/megaphone-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuSettings.AppendItem( self.menuAlarm )
        
        self.menuSerial = wx.MenuItem( self.menuSettings, wx.ID_ANY, u"Serial port", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSerial.SetBitmap( wx.Bitmap( u"./icons/port-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuSettings.AppendItem( self.menuSerial )
        
        self.menuEcoMode = wx.MenuItem( self.menuSettings, wx.ID_ANY, u"Enable Eco Mode", wx.EmptyString, wx.ITEM_CHECK )
        self.menuSettings.AppendItem( self.menuEcoMode )       
        
        self.menuFile.AppendSubMenu( self.menuSettings, u"Settings" )
        
        self.menuRecords = wx.MenuItem( self.menuFile, wx.ID_ANY, u"Records", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuRecords.SetBitmap( wx.Bitmap( u"./icons/Folder-Chart-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuFile.AppendItem( self.menuRecords )
        
        self.menuDTC = wx.MenuItem( self.menuFile, wx.ID_ANY, u"Diganostic Trouble Code", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuDTC.SetBitmap( wx.Bitmap( u"./icons/Transport-Engine-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuFile.AppendItem( self.menuDTC )
        
        self.menuFile.AppendSeparator()
        
        self.menuModes = wx.Menu()
        self.menuGraphical = wx.MenuItem( self.menuModes, wx.ID_ANY, u"Graphical", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuGraphical.SetBitmap( wx.Bitmap( u"./icons/speedometer-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuModes.AppendItem( self.menuGraphical )
        
        self.menuNumerical = wx.MenuItem( self.menuModes, wx.ID_ANY, u"Numerical", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuNumerical.SetBitmap( wx.Bitmap( u"./icons/Industry-Display-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuModes.AppendItem( self.menuNumerical )
        
        self.menuSensorList = wx.MenuItem( self.menuModes, wx.ID_ANY, u"Sensor List", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSensorList.SetBitmap( wx.Bitmap( u"./icons/Data-List-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuModes.AppendItem( self.menuSensorList )
        
        self.menuFile.AppendSubMenu( self.menuModes, u"Modes" )
        
        self.menuQuit = wx.MenuItem( self.menuFile, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuQuit.SetBitmap( wx.Bitmap( u"./icons/Actions-dialog-cancel-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuFile.AppendItem( self.menuQuit )
        
        self.menubar.Append( self.menuFile, u"File" ) 
        
        menuView = wx.Menu()
        self.menuStatus = wx.MenuItem( menuView, wx.ID_ANY, u"Show Status Bar", wx.EmptyString, wx.ITEM_CHECK )
        self.shst = menuView.AppendItem( self.menuStatus )
        
        menuView.Check(self.shst.GetId(), True) 
        
        
        self.menubar.Append( menuView, u"View" ) 
        
        self.menuHelp = wx.Menu()
        self.menuAbout = wx.MenuItem( self.menuHelp, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuAbout.SetBitmap( wx.Bitmap( u"./icons/Actions-help-about-icon.png", wx.BITMAP_TYPE_ANY ) )
        self.menuHelp.AppendItem( self.menuAbout )
        
        self.menubar.Append( self.menuHelp, u"Help" ) 
        
        self.SetMenuBar( self.menubar )
        


        self.panelLoading = OBDLoadingPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panelLoading, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.panelLoading.showLoadingScreen()
        self.panelLoading.SetFocus()
        #OBDLoadingPanel.gif.Play(False)
        
        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnSensors, id = self.menuSensors.GetId() )
        self.Bind( wx.EVT_MENU, self.OnRecords, id = self.menuRecords.GetId() )
        self.Bind( wx.EVT_MENU, self.OnAlarms, id = self.menuAlarm.GetId() )
        self.Bind( wx.EVT_MENU, self.OnEcoMode, id = self.menuEcoMode.GetId() )
        self.Bind( wx.EVT_MENU, self.OnRecordsSettings, id = self.menuRecordsSettings.GetId() )
        self.Bind( wx.EVT_MENU, self.OnDTC, id = self.menuDTC.GetId() )
        self.Bind( wx.EVT_MENU, self.OnGraphical, id = self.menuGraphical.GetId() )
        self.Bind( wx.EVT_MENU, self.OnNumerical, id = self.menuNumerical.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSensorList, id = self.menuSensorList.GetId() )
        self.Bind( wx.EVT_MENU, self.OnQuit, id = self.menuQuit.GetId() )
        self.Bind( wx.EVT_MENU, self.ToggleStatusBar, id = self.menuStatus.GetId() )
        self.Bind( wx.EVT_MENU, self.OnAbout, id = self.menuAbout.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSerial, id = self.menuSerial.GetId() )
        self.Bind(wx.EVT_TIMER, self.UpdateTime, self.timer)
        self.Bind(wx.EVT_TIMER, self.UpdateDTC, self.timerDTC)

        
        #panels
        self.settingsesorpanel = SettitingSensorPanel(self)
        self.settingalarmpanel = SettingAlarmsPanel(self)
        self.settingserialpanel = SettingSerialPanel(self)
        self.settingrecordpanel = SettingRecordPanel(self)
        self.modegraphicalpanel = ModeGraphicalPanel(self)
        self.dtcpanel = DTCsPanel(self)
        self.recordspanel = RecordsPanel(self)
        self.modelistpanel = ModeListPanel(self)
        self.modenumericalpanel = ModeNumericalPanel(self)
        
        if self.menuEcoMode.IsChecked():
            self.ecomode = True
      
        else:
            self.ecomode = False  

        self.cfg = wx.Config('DTCs Settings')
        if self.cfg.Exists('refresh'): #port baudrate databits parity stop bits
            refreshtime = self.cfg.ReadInt('refresh')
            autodtc = self.cfg.ReadInt('autodtc')
            
            if autodtc == 1:
                self.timerDTC.Start(refreshtime*1000) 
            else:
                self.timerDTC.Stop()  
        else:        
            autodtc = 0
            
                  
        
        
        #eventes
    def OnSensors(self,event):
        self.DestroyActivePanel()    
                
        self.statusbar.SetStatusText('sensors selected')
        self.settingsesorpanel = SettitingSensorPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.settingsesorpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues()
        self.settingsesorpanel.setSensors(self.sensors)
        self.settingsesorpanel.showSettingSensorPanel()
        self.settingsesorpanel.SetFocus()
        self.Layout()
        
        
    def OnAlarms(self,event):
        self.DestroyActivePanel() 
                    
        self.statusbar.SetStatusText('alarms selected')
        self.settingalarmpanel = SettingAlarmsPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.settingalarmpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues()
        self.settingalarmpanel.setSensors(self.sensors)
        self.settingalarmpanel.showAlarmPPanel()
        self.settingalarmpanel.SetFocus()
        self.Layout()
    
    def OnRecords(self,event):
        self.DestroyActivePanel() 
                
        self.statusbar.SetStatusText('records selected')
        self.recordspanel = RecordsPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.recordspanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues()
        self.recordspanel.setSensors(self.sensors)
        self.recordspanel.showRecordsPanel()
        self.recordspanel.SetFocus()
        self.Layout()
        
    def OnEcoMode(self, event):        
        if self.menuEcoMode.IsChecked():
            self.statusbar.SetStatusText('Eco Mode On')
            self.ecomode = True
            
      
        else:
            self.statusbar.SetStatusText('Eco Mode Off')
            self.menuEcoMode.SetBitmap( wx.Bitmap( u"./icons/Heart-gray-icon.png", wx.BITMAP_TYPE_ANY ) ) 
            self.ecomode = False
        
    def update(self,event):
        self.path= os.path.dirname(__file__)
        self.record_path = os.path.join(self.path, 'recrods/')
        self.filedate = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')       
        self.record_file = "records-" +self.filedate +".csv" + "\n"
        f = open(self.record_file, 'w')
        f.close()
        
        if not os.path.isdir(self.record_path):
            os.makedirs(self.record_path)
            
        if self.panelLoading:
            connection = self.panelLoading.getConnection()
            sensors = self.panelLoading.getSensors()
            port = self.panelLoading.getPort()
            c = self.panelLoading.getClass()
            self.panelLoading.Destroy()
            print ('in update')
	    print (connection)
        print (sensors)
        print (port)       
        
        if connection:
            print 'if connection'
            self.modenumericalpanel.setConnection(connection)
            self.modelistpanel.setConnection(connection)
            self.modegraphicalpanel.setConnection(connection)
       
        if sensors:    
            print 'sending sensors and port'
            self.modenumericalpanel.setSensors(sensors)
            self.modenumericalpanel.setPort(port)
            
            self.modegraphicalpanel.setSensors(sensors)
            self.modegraphicalpanel.setPort(port)
            self.modelistpanel.setSensors(sensors)
            self.modelistpanel.setPort(port)
            self.modenumericalpanel.setEcoMode(self.ecomode)
            self.modegraphicalpanel.setEcoMode(self.ecomode)
            self.modelistpanel.setEcoMode(self.ecomode)  
 
            self.modelistpanel.setRecordFile(self.record_file)
            self.setvalues(sensors, port)
            self.dtcpanel.setPort(port)
 
            print 'sens and p gotten'
            self.setvalues(sensors, port)
            self.setclass(c) 
        
        self.modenumericalpanel = ModeNumericalPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modenumericalpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues()
        self.modenumericalpanel.setPort(self.port)
        self.modenumericalpanel.setSensors(self.sensors)
        self.modegraphicalpanel.setEcoMode(self.ecomode)
        self.modenumericalpanel.showModeNumericalPanel()
        self.modenumericalpanel.ShowSensors()
        self.modenumericalpanel.SetFocus()
        self.Layout()
    
    def setvalues(self, sensors, port):
        self.sensors = sensors
        self.port = port     
    
    def setclass (self, c):
        self.c= c
    
    def getvalues (self):
        return self.sensors, self.port  
    
    def getport (self):
        return self.port
    
    def getsensor (self):
        return self.sensors  
    
    def getClass (self):
        return self.c
    
    
    def OnSerial(self, etent):
        self.DestroyActivePanel() 
             
        self.statusbar.SetStatusText('Serial Setting selected')    
        self.settingserialpanel = SettingSerialPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.settingserialpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.settingserialpanel.showSerialPanel()
        self.settingserialpanel.SetFocus()
        self.Layout()
        
    def OnSettings (self, event):
        self.statusbar.SetStatusText('settings selected')      
    
    def OnRecordsSettings (self, event):
        self.DestroyActivePanel() 
                
        self.statusbar.SetStatusText('records settings selected')
        self.settingrecordpanel = SettingRecordPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.settingrecordpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.sensors, self.port = self.getvalues()
        self.settingrecordpanel.setSensors(self.sensors)
        self.settingrecordpanel.showSettingRecordPanel()
        self.settingrecordpanel.SetFocus()
        self.Layout()
        
    def OnDTC (self, event):
        self.DestroyActivePanel()   
        self.statusbar.SetStatusText('DTC selected')
        self.dtcpanel = DTCsPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.dtcpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.port = self.getport()
        getclass = self.getClass() 
        self.dtcpanel.setClass(getclass)
        self.dtcpanel.setPort(self.port)
        self.dtcpanel.showDTCsPanel()
        self.dtcpanel.SetFocus()
        self.Layout()
    
        
    def OnGraphical (self, event):
        self.DestroyActivePanel()     
        self.statusbar.SetStatusText('Graphical selected')
        self.modegraphicalpanel = ModeGraphicalPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modegraphicalpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues() 
        self.modegraphicalpanel.setPort(self.port)
        self.modegraphicalpanel.setSensors(self.sensors)
        self.modegraphicalpanel.setEcoMode(self.ecomode)
        self.modegraphicalpanel.showGraphicalPanel()
        self.modegraphicalpanel.ShowSensors()
        self.modegraphicalpanel.SetFocus()
        self.Layout()
        
        
    def OnNumerical (self, event):
        self.statusbar.SetStatusText('Numerical selected')
        self.DestroyActivePanel() 
       
        self.modenumericalpanel = ModeNumericalPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modenumericalpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues()  
        self.modenumericalpanel.setPort(self.port)
        self.modenumericalpanel.setSensors(self.sensors)
        self.modenumericalpanel.setEcoMode(self.ecomode)
        self.modenumericalpanel.showModeNumericalPanel()
        self.modenumericalpanel.ShowSensors()
        self.modenumericalpanel.SetFocus()
        self.Layout()
        
    def OnSensorList (self, event):
        self.statusbar.SetStatusText('Sensor list selected')
        self.DestroyActivePanel() 
            
        self.modelistpanel = ModeListPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modelistpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sensors, self.port = self.getvalues()
        self.modelistpanel.setRecordFile(self.record_file) 
        self.modelistpanel.setPort(self.port)
        self.modelistpanel.setEcoMode(self.ecomode)
        self.modelistpanel.showModeListPanel()
        self.modelistpanel.ShowSensors()
        self.modelistpanel.SetFocus()
        self.Layout()
    
    
    
    def OnAbout (self, event):
        # A message dialoge box with an OK button. wx.OK is a sandard ID in wxWidgets u"PFC Desarrollo de Sistema Electrónico de Información y Diagnosis con Pantalla Táctil para Vehículos con EOBD \n\nAuthor: Bernardo Plaza\nVersion: 1.0", wx.DefaultPosition, wx.DefaultSize, 0 )
        dialog = wx.MessageDialog(self, u"PFC Desarrollo de Sistema Electrónico de Información y Diagnosis con Pantalla Táctil para Vehículos con EOBD \n\nAuthor: Bernardo Plaza\nVersion: 1.0")
        dialog.ShowModal()  # show it
        dialog.Destroy()  # finally destroy it when finished
        self.statusbar.SetStatusText('About selected')
        
    def DestroyActivePanel(self):
        if self.panelLoading:
            self.panelLoading.Destroy()
        if  self.settingsesorpanel:
            self.settingsesorpanel.Destroy()         
        if self.settingrecordpanel:
            self.settingrecordpanel.Destroy() 
        if self.settingalarmpanel:
            self.settingalarmpanel.Destroy()
        if self.settingserialpanel:
            self.settingserialpanel.Destroy()     
        if self.recordspanel:
            self.recordspanel.Destroy() 
            autodtc=0
        if self.dtcpanel:
            self.dtcpanel.Destroy()
            if self.cfg.Exists('refresh'): #port baudrate databits parity stop bits
                refreshtime = self.cfg.ReadInt('refresh')
                autodtc = self.cfg.ReadInt('autodtc')
            
            if autodtc == 1:
                self.timerDTC.Start(refreshtime*1000) 
                
            else:
                self.timerDTC.Stop()  
                  
       
        if self.modegraphicalpanel:
            self.modegraphicalpanel.Destroy()   
        if self.modenumericalpanel:
            self.modenumericalpanel.Destroy()
        if self.modelistpanel:
            self.modelistpanel.Destroy()      
             
    def UpdateTime(self,event):
        self.statusbar.SetStatusText(datetime.now().strftime("%d-%m-%Y %H:%M:%S"),1)
    
    def UpdateDTC(self,event):
        print 'DTC timer'
        getclass = self.getClass() 
        self.DTCCodes = getclass.get_dtc()
        if self.DTCCodes : 
            wx.MessageBox('List of DTCs' + str(self.DTCCodes), 'DTC Codes', wx.OK | wx.ICON_INFORMATION)
               
            
    def ToggleStatusBar(self, e):
        
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()
           
    
    
    def OnQuit(self, e):
        self.Close()
 
 
    def __del__(self):
        pass    
            

class PFCApp(wx.App):
    """
    OBD Application.
    """

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        """
        Constructor.
        """
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        """
        Initializer.
        """
        # Main frame                                           
        frame = PFCFrame()
        self.SetTopWindow(frame)
        
        #frame.ShowFullScreen(True)
        frame.Show(True)
        #frame.showLoadingPanel()



        return True

    def FilterEvent(self, event):
        if event.GetEventType == wx.KeyEvent:
            pass

#-------------------------------------------------------------------------------




app = PFCApp(0)
app.MainLoop()

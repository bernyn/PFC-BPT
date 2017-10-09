# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import os
import wx
import wx.xrc
import wx.animate
import obd_sensors
from settingserial import SettingSerialPanel
from settingsensor import SettitingSensorPanel
from settinglarm import SettingAlarmsPanel
from settingrecords import SettingRecordPanel
from modegraphical import ModeGraphicalPanel
#from modenumerical import ModeNumericalPanel
from records import RecordsPanel
from DTCs import DTCsPanel
from modelist import ModeListPanel

from datetime import datetime
import time

from obd_capture import OBD_Capture
from obd_sensors import SENSORS
from obd_sensors import *
from threading import Thread


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

    def is_connected(self):
        return self.c.is_connected()

    def get_output(self):
        if self.c and self.c.is_connected():
            return self.c.capture_data()
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
        return sensors

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
        

class PanelMain(wx.Panel):
    """
    Panel for gauges.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        super(PanelMain, self).__init__(*args, **kwargs)
        
        boxSizer = wx.BoxSizer(wx.VERTICAL)

        self.textCtrl = OBDText(self)
        boxSizer.Add(self.textCtrl, 1,  wx.ALIGN_CENTER_VERTICAL, 0)
        font3 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL, faceName="Monaco")
        self.textCtrl.SetFont(font3)
        self.textCtrl.AddText(" Panel Principal\n")    
        
        self.SetSizer(boxSizer)
        self.Centre()
        self.Show(True)
   
        
        self.Layout() 
        self.SetBackgroundColour(wx.NullColour)
        self.SetForegroundColour(wx.NullColour) 
        self.Refresh()

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
        while not connected:
            connected = self.c.is_connected()
            self.textCtrl.Clear()
            #self.textCtrl.AddText(" Trying to connect ..." + time.asctime())
            self.textCtrl.AddText("Trying to connect ..." + time.asctime())
            if connected: 
                break
                print('waiting')
            if __debug__:
                print "In debug mode"
                time_delta = datetime.now() - start_time
                if time_delta.seconds >= 0.1:
                    break
                        

        if not connected:
            self.textCtrl.AddText(" Not connected\n")
            return False
        else:
            #self.textCtrl.Clear()
            #self.textCtrl.AddText(" Connected\n")
            port_name = self.c.get_port_name()
            if port_name:
                self.textCtrl.AddText(" Failed Connection: " + port_name +"\n")
                self.textCtrl.AddText(" Please hold alt & esc to view terminal.")
            self.textCtrl.AddText(str(self.c.get_output()))
            self.sensors = self.c.get_sensors()
            self.port = self.c.get_port()

            self.GetParent().update(None)


    def getSensors(self):
        return self.sensors
    
    def getPort(self):
        return self.port

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
        #self.menuEcoMode.SetBitmap( wx.Bitmap( u"./icons/Heart-green-icon.png", wx.BITMAP_TYPE_ANY ) )
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
        self.recordspanel.showRecordsPanel()
        self.recordspanel.SetFocus()
        self.Layout()
        
    def OnEcoMode(self, e):        
        if self.menuEcoMode.IsChecked():
            self.statusbar.SetStatusText('Eco Mode On')
            #self.menuEcoMode.SetBitmap( wx.Bitmap( u"./icons/Heart-green-icon.png", wx.BITMAP_TYPE_ANY ) )
        else:
            self.statusbar.SetStatusText('Eco Mode Off')
            self.menuEcoMode.SetBitmap( wx.Bitmap( u"./icons/Heart-gray-icon.png", wx.BITMAP_TYPE_ANY ) )   
        
    def update(self,event):
        if self.panelLoading:
            connection = self.panelLoading.getConnection()
            sensors = self.panelLoading.getSensors()
            port = self.panelLoading.getPort()
            self.panelLoading.Destroy()
            
        self.modenumericalpanel = ModeNumericalPanel(self)
        
        if sensors:
            self.modenumericalpanel.setSensors(sensors)
            self.modenumericalpanel.setPort(port)        
        
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modelistpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.modenumericalpanel.showModeNumericalPanel()
        self.modenumericalpanel.ShowSensors()
        self.modenumericalpanel.SetFocus()
        self.Layout()
    
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
        self.modegraphicalpanel.showGraphicalPanel()
        self.modegraphicalpanel.SetFocus()
        self.Layout()
        
        
    def OnNumerical (self, event):
        self.statusbar.SetStatusText('Numerical selected')
        self.DestroyActivePanel() 
        
        self.modenumericalpanel = ModeNumericalPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modenumericalpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
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
        self.modelistpanel.showModeListPanel()
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
        event.Skip()
    
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

#4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~4~~~
class ModeNumericalPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeNumericalPanel, self).__init__(*args, **kwargs)

    def showModeNumericalPanel(self):           
        
        #self.value = 2.88
        
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
        self.sensors = []
        
        # Port 
        self.port = None

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
        return sensors_display

    def ShowSensors(self):
        """
        Display the sensors.
        """
        print 'showsensors'
        sensors = self.getSensorsToDisplay(self.istart)

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

   




#####4~~4~~4~~4~~4~~4~~4~~


app = PFCApp(0)
app.MainLoop()
# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from datetime import datetime

import wx
import wx.animate
import wx.xrc

from DTCs import DTCsPanel
from modegraphical import ModeGraphicalPanel
from modelist import ModeListPanel
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


###########################################################################
## Class frameInit
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
       # self.SetForegroundColour(wx.WHITE)  

        font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL, faceName="Monaco")
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

        
    def showLoadingScreen(self):
        """
        Display the loading screen.
        """
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        gif_fname = u"./icons/loading 80.gif" 
        self.gif = wx.animate.GIFAnimationCtrl(self, wx.ID_ANY, gif_fname, pos=(-1, -1))
        self.gif.GetPlayer().UseBackgroundColour(True)
        self.gif.Play()
        boxSizer.Add(self.gif, 1, wx.ALIGN_CENTER_HORIZONTAL,  0)
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
        self.timer0.Start(500)

    def connect(self, event):
        if self.timer0:
            self.timer0.Stop()
        self.textCtrl.AddText(" doing things...\n")   
        self.GetParent().update(None)

   
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
        self.menuEcoMode.SetBitmap( wx.Bitmap( u"./icons/Heart-green-icon.png", wx.BITMAP_TYPE_ANY ) )
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
            self.panelLoading.Destroy()   
            
        self.modelistpanel = ModeListPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modelistpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.modelistpanel.showModeListPanel()
        self.modelistpanel.SetFocus()
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
        #if self.panelmain:
            #self.panelmain.Destroy()
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
        #if panelID == PANEL_RECORDS:
            #print 'destroy record panel'
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
        #if panelID == PANEL_MODE_NUMERICAL :
            #print 'destroy numerical panel'   
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

        # This frame is used only to set the full screen mode  
        # for the splash screen display and for transition with 
        # the loading screen.
        # This frame is not shown and will be deleted later on.
        #frame0 = OBDFrame0()
        #self.SetTopWindow(frame0)
        #frame0.ShowFullScreen(True)
        #self.SetTopWindow(frame0)

        # Splash screen
        #splash = OBDSplashScreen(frame0, frame0)
        #self.SetTopWindow(splash)
        #splash.Show(True)
        #splash.ShowFullScreen(True)

        return True

    def FilterEvent(self, event):
        if event.GetEventType == wx.KeyEvent:
            pass

#-------------------------------------------------------------------------------




app = PFCApp(0)
app.MainLoop()
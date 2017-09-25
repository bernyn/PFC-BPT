#SELECTOR MULTIPLE
from pylab import plotfile, show, gca
import matplotlib.cbook as cbook

import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import obd_sensors

 
     
class ModeNumericalPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeNumericalPanel, self).__init__(*args, **kwargs)

    def showModeNumericalPanel(self):           
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Sensor Numerical Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer9.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 1 )
               
        
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
        
        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        bSizer2.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )


    def setConnection(self, connection):
        self.connection = connection
    
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def setPort(self, port):
        self.port = port

    def getSensorsToDisplay(self, istart):
        """
        Get at most 6 sensors to be display on screen.
        """
        sensors_display = []
        if istart<len(self.sensors):
            iend = istart + 6
            sensors_display = self.sensors[istart:iend]
        print sensors_display
        return sensors_display

    def ShowSensors(self):
        """
        Display the sensors.
        """
        
        sensors = self.getSensorsToDisplay(self.istart)

        # Destroy previous widgets
        for b in self.boxes: b.Destroy()
        for t in self.texts: t.Destroy()
        self.boxes = []
        self.texts = []

        # Main sizer
        boxSizerMain = wx.BoxSizer(wx.VERTICAL)

        # Grid sizer
        nrows, ncols = 2, 3
        vgap, hgap = 50, 50
        gridSizer = wx.GridSizer(nrows, ncols, vgap, hgap)

        # Create a box for each sensor
        for index, sensor in sensors:
            
            (name, value, unit) = self.port.sensor(index)

            box = OBDStaticBox(self, wx.ID_ANY)
            self.boxes.append(box)
            boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)

            # Text for sensor value 
            if type(value)==float:  
                value = str("%.2f"%round(value, 3))   
                                
            t1 = wx.StaticText(parent=self, label=str(value), style=wx.ALIGN_CENTER)
            t1.SetForegroundColour('WHITE')
            font1 = wx.Font(32, wx.ROMAN, wx.NORMAL, wx.NORMAL, faceName="Monaco")
            t1.SetFont(font1)
            boxSizer.Add(t1, 0, wx.ALIGN_CENTER | wx.ALL, 20)
            boxSizer.AddStretchSpacer()
            self.texts.append(t1)

            # Text for sensor name
            t2 = wx.StaticText(parent=self, label=unit+"\n"+name, style=wx.ALIGN_CENTER)
            t2.SetForegroundColour('WHITE')
            font2 = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, faceName="Monaco")
            t2.SetFont(font2)
            boxSizer.Add(t2, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            self.texts.append(t2)
            gridSizer.Add(boxSizer, 1, wx.EXPAND | wx.ALL)
            
            print value
            print t2  

        # Add invisible boxes if necessary
        nsensors = len(sensors)
        for i in range(6-nsensors):
            box = OBDStaticBox(self)
            boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            self.boxes.append(box)
            box.Show(False)
            gridSizer.Add(boxSizer, 1, wx.EXPAND | wx.ALL)
           
        # Layout
        boxSizerMain.Add(gridSizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(boxSizerMain)
        self.Refresh()
        self.Layout() 

        # Timer for update
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)
        self.timer.Start(2000)


    def refresh(self, event):
        sensors = self.getSensorsToDisplay(self.istart)   
        
        itext = 0
        for index, sensor in sensors:

            (name, value, unit) = self.port.sensor(index)
            if type(value)==float:  
                value = str("%.2f"%round(value, 3))                    

            if itext<len(self.texts):
                self.texts[itext*2].SetLabel(str(value))
            print ('Name= ' + name + ', Value= '+ value) 
            itext += 1


    def onCtrlC(self, event):
        self.GetParent().Close()

    def onLeft(self, event):
        """
        Get data from 6 previous sensors in the list.
        """
        istart = self.istart-6 
        if istart<0: istart = 0
        self.istart = istart
        self.ShowSensors()

    def onRight(self, event):
        """
        Get data from 6 next sensors in the list.
        """
        istart = self.istart+6
        if istart<len(self.sensors):
            self.istart = istart
            self.ShowSensors()


class OBDStaticBox(wx.StaticBox):
    """
    OBD StaticBox.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.StaticBox.__init__(self, *args, **kwargs)
#SELECTOR MULTIPLE
import sys

from pylab import plotfile, show, gca
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

import matplotlib.cbook as cbook
import obd_sensors


class ModeListPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeListPanel, self).__init__(*args, **kwargs)

    def showModeListPanel(self):           
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Sensor List Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer9.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 1 )
               
        
        #=======================================================================
        # panelList = wx.Panel( self, -1 )
        # leftPanel = wx.Panel(panelSettings, -1)
        #=======================================================================
        
        self.list = wx.ListCtrl(self.m_panel1, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list.InsertColumn(0, 'Name', width=140)
        self.list.InsertColumn(1, 'Value')
        self.list.InsertColumn(1, 'Units')
                   
         
        self.cfg = wx.Config('sensorsettings')
        num = self.list.GetItemCount()
       
        if self.cfg.Exists('Supported PIDs'):             
            print ("confg load")
            
                
            for i,e in enumerate(obd_sensors.SENSORS):
                 
                if self.cfg.ReadBool(e.name)==True:
                    index = self.list.InsertStringItem(sys.maxint, e.name)
                    self.list.SetStringItem(index, 1, 'fake val')
                    self.list.SetStringItem(index, 2, e.unit)                  
         
        else:
            print'empty list'
        
  
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
         

    
# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from datetime import datetime

import wx
import wx.xrc

from obd_capture import OBD_Capture

GET_DTC_COMMAND   = "03"
             
class DTCsPanel( wx.Panel ):
    
    def __init__(self, *args, **kwargs):
        #config values
        super(DTCsPanel, self).__init__(*args, **kwargs)

        
    def showDTCsPanel(self):            
        #init
        
        self.cfg = wx.Config('DTCs Settings')
        if self.cfg.Exists('refresh'): #port baudrate databits parity stop bits
            refreshtime = self.cfg.ReadInt('refresh')
            autodtc = self.cfg.ReadInt('autodtc')
            
        else:
            refreshtime = 50000
            autodtc = 0
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Diagnostic Trouble Codes", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer9.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 1 )
        
        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 1 )
        
        self.dtcText = wx.TextCtrl(self.m_panel1,size = (-1,80),style = wx.TE_MULTILINE) 
        bSizer9.Add(self.dtcText,1, wx.EXPAND|wx.ALL,1) 
              
        
        hSizer1 = wx.BoxSizer( wx.HORIZONTAL )
         
        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Auto DTC read time (s)", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
         
        hSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
         
        self.refreshtimebox = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 3600, 0 )
        hSizer1.Add( self.refreshtimebox, 0, wx.ALL, 5 )
        self.refreshtimebox.SetValue(refreshtime) 
        
        self.aDTCtime = wx.CheckBox( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        hSizer1.Add( self.aDTCtime, 0, wx.ALL, 5 )
        self.aDTCtime.SetValue(autodtc)  
        
        
        self.aDTCtimeT = wx.StaticText( self.m_panel1, wx.ID_ANY, u"On/Off", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.aDTCtimeT.Wrap( -1 )
        self.aDTCtimeT.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        hSizer1.Add( self.aDTCtimeT, 0, wx.ALL, 5 )
        
             
        bSizer9.Add( hSizer1, 1, wx.EXPAND, 0 )
                
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.readDTCbutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Read DTC", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer7.Add( self.readDTCbutton, 0,  wx.EXPAND,5 )
        
        self.readDTCFbutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Read Freeze DTC", wx.DefaultPosition,  wx.Size( -1,-1 ), 0 )
        bSizer7.Add( self.readDTCFbutton, 0,  wx.EXPAND, 5 )
        
        self.clearDTCbutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Clear DTC", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        bSizer7.Add( self.clearDTCbutton, 0,  wx.EXPAND,5 )
        
        self.saveDTCTime = wx.Button( self.m_panel1, wx.ID_ANY, u"Save Config", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer7.Add( self.saveDTCTime, 0,  wx.EXPAND,5 )
        
        bSizer9.Add( bSizer7, 1, wx.EXPAND, 0 )
        
        
        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        bSizer2.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
        
        # Port 
        self.port = None
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        self.capture= OBD_Capture
        
        # Connect Events

        self.saveDTCTime.Bind( wx.EVT_BUTTON, self.OnSaveDTC)
        self.readDTCbutton.Bind( wx.EVT_BUTTON, self.OnReadDTC )
        self.readDTCFbutton.Bind( wx.EVT_BUTTON, self.OnReadDTCF )
        self.clearDTCbutton.Bind( wx.EVT_BUTTON, self.OnClearDTC )
        #self.serialbackbutton.Bind( wx.EVT_BUTTON, self.OnSerialBack )
    
    def setPort(self, port):
        self.port = port
        
        
    def getPort(self):
        return self.port
        
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def OnSaveDTC (self,event):
        self.cfg.WriteInt("refresh", self.refreshtimebox.GetValue())
        autodtc= self.aDTCtime.Get3StateValue()
        self.cfg.WriteInt("autodtc", autodtc)
        self.dtcText.AppendText(('Conf saved on ')+ datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    def OnReadDTC( self, event ):    
        self.DTCCodes = self.capture.capture_dtc()
        print self.DTCCodes
        self.dtcText.AppendText('List of DTCs' + str(self.DTCCodes))

   
    def OnReadDTCF( self, event ):
        self.DTCCodes = self.capture.capture_dtc()
        self.dtcText.AppendText('List of DTCs' + str(self.DTCCodes))
    
    def OnClearDTC( self, event ):
        self.DTCCodes = self.capture.clear_dtc()
        print self.DTCCodes
        self.dtcText.AppendText('List of DTCs' + str(self.DTCCodes))
        
    
    def OnSerialBack( self, event ):
        self.dtcText.Clear()
        event.Skip()


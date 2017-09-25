# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import wx
import wx.xrc
             
class SettingSerialPanel( wx.Panel ):
    
    def __init__(self, *args, **kwargs):
        #config values
        super(SettingSerialPanel, self).__init__(*args, **kwargs)

        
    def showSerialPanel(self):            
        #init
        self.cfg = wx.Config('serialsettings')
        if self.cfg.Exists('port'): #port baudrate databits parity stop bits
            port, baudrate, databits = self.cfg.ReadInt('port'), self.cfg.ReadInt('baudrate'), self.cfg.ReadInt('databits')
            parity, stopbits = self.cfg.ReadInt('parity'), self.cfg.ReadInt('stopbits')
 
        else:
            (port, baudrate, databits, parity, stopbits) = (0, 0, 3, 0, 0)
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Serial Port Configuration", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer9.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 1 )
        
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        comPortConfChoices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9", u"COM10" ]
        self.comPortConf = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, comPortConfChoices, 0 )
        self.comPortConf.SetSelection( port )
        self.comPortConf.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.comPortConf, 0, wx.ALL, 0 )
        
        self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Baud Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        self.m_staticText4.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        baudRateConfChoices = [ u"9600", u"38400", u"115200" ]
        self.baudRateConf = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, baudRateConfChoices, 0 )
        self.baudRateConf.SetSelection( baudrate )
                    
        self.baudRateConf.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.baudRateConf, 0, wx.ALL, 0 )
        
        self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Data Bits", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        self.m_staticText5.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        dataBitsConfChoices = [ u"5", u"6", u"7", u"8" ]
        self.dataBitsConf = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, dataBitsConfChoices, 0 )
        self.dataBitsConf.SetSelection( databits )       
        
        self.dataBitsConf.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.dataBitsConf, 0, wx.ALL, 0 )
        
        self.m_staticText6 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Parity", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        self.m_staticText6.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
        
        parityConfChoices = [ u"none", u"even", u"odd", u"mark", u"space", wx.EmptyString ]
        self.parityConf = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, parityConfChoices, 0 )
        self.parityConf.SetSelection( parity )
        self.parityConf.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.parityConf, 0, wx.ALL, 0 )
        
        self.m_staticText7 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Stop Bits", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        stopbitsConfChoices = [ u"0", u"1", u"1.5", u"2" ]
        self.stopBitsConf = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"asd", wx.DefaultPosition, wx.DefaultSize, stopbitsConfChoices, 0 )
        self.stopBitsConf.SetSelection( stopbits )
        self.stopBitsConf.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        
        gSizer1.Add( self.stopBitsConf, 0, wx.ALL, 0 )
        
        
        bSizer9.Add( gSizer1, 1, wx.EXPAND, 1 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.serialsavebutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer7.Add( self.serialsavebutton, 0,  wx.EXPAND,5 )
        
        self.serialtestbutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer7.Add( self.serialtestbutton, 0,  wx.EXPAND, 5 )
        
        self.serialdefaultbutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Default", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer7.Add( self.serialdefaultbutton, 0,  wx.EXPAND,5 )
        
        #=======================================================================
        # self.serialbackbutton = wx.Button( self.m_panel1, wx.ID_ANY, u"Back", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        # bSizer7.Add( self.serialbackbutton, 0,  wx.EXPAND, 5 )
        #=======================================================================
        
        
        bSizer9.Add( bSizer7, 1, wx.EXPAND, 0 )
        
        
        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        bSizer2.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events

        self.serialsavebutton.Bind( wx.EVT_BUTTON, self.OnSerialSave )
        self.serialtestbutton.Bind( wx.EVT_BUTTON, self.OnSerialTest )
        self.serialdefaultbutton.Bind( wx.EVT_BUTTON, self.OnSerialDefault )
        #self.serialbackbutton.Bind( wx.EVT_BUTTON, self.OnSerialBack )
    
        
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def OnSerialSave( self, event ):
        portconf= self.comPortConf.GetSelection() 
        baudconf = self.baudRateConf.GetSelection()
        databitsconf = self.dataBitsConf.GetSelection()    
        parityconf= self.parityConf.GetSelection()     
        stopbitsconf= self.stopBitsConf.GetSelection()

        self.cfg.WriteInt("port", portconf)
        self.cfg.WriteInt("baudrate", baudconf)
        self.cfg.WriteInt("databits", databitsconf)
        self.cfg.WriteInt("parity", parityconf)
        self.cfg.WriteInt("stopbits", stopbitsconf)
        self.statusBar.SetStatusText('Configuration saved, %s ' % wx.Now())
    
    def OnSerialTest( self, event ):
        event.Skip()
    
    def OnSerialDefault( self, event ):
        self.comPortConf.SetSelection(0) 
        self.baudRateConf.SetSelection(0)
        self.dataBitsConf.SetSelection(3)    
        self.parityConf.SetSelection(0)     
        self.stopBitsConf.SetSelection(0)
        
        
    
    #===========================================================================
    # def OnSerialBack( self, event ):
    #     event.Skip()
    #===========================================================================


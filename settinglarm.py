# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import obd_sensors


###########################################################################
## Class frameSettingAlarmScroll
###########################################################################
class SettingAlarmsPanel ( wx.Panel ):
    
        
    def __init__(self, *args, **kwargs):
        #config values
        super(SettingAlarmsPanel, self).__init__(*args, **kwargs)

    
    def showAlarmPPanel(self): 
        #init
        self.cfg = wx.Config('alarmsettings')
        if self.cfg.Exists('alarm1minstatus'):  
            alarm1mins, alarm1minval, alarm1Maxs,alarm1Maxval = self.cfg.ReadInt('alarm1minstatus'), self.cfg.ReadInt('alarm1minvalue'),self.cfg.ReadInt('alarm1Maxstatus'), self.cfg.ReadInt('alarm1Maxvalue')    
            alarm2mins, alarm2minval, alarm2Maxs,alarm2Maxval = self.cfg.ReadInt('alarm2minstatus'), self.cfg.ReadInt('alarm2minvalue'),self.cfg.ReadInt('alarm2Maxstatus'), self.cfg.ReadInt('alarm2Maxvalue')
            alarm3mins, alarm3minval, alarm3Maxs,alarm3Maxval = self.cfg.ReadInt('alarm3minstatus'), self.cfg.ReadInt('alarm3minvalue'),self.cfg.ReadInt('alarm3Maxstatus'), self.cfg.ReadInt('alarm3Maxvalue')
            alarm4mins, alarm4minval, alarm4Maxs,alarm4Maxval = self.cfg.ReadInt('alarm4minstatus'), self.cfg.ReadInt('alarm4minvalue'),self.cfg.ReadInt('alarm4Maxstatus'), self.cfg.ReadInt('alarm4Maxvalue')
            alarm5mins, alarm5minval, alarm5Maxs,alarm5Maxval = self.cfg.ReadInt('alarm5minstatus'), self.cfg.ReadInt('alarm5minvalue'),self.cfg.ReadInt('alarm5Maxstatus'), self.cfg.ReadInt('alarm5Maxvalue')
            alarm1t, alarm2t, alarm3t, alarm4t, alarm5t = self.cfg.Read('alarm1'), self.cfg.Read('alarm2'), self.cfg.Read('alarm3'), self.cfg.Read('alarm4'), self.cfg.Read('alarm5')
        else:
            posta1, alarm1mins, alarm1minval, alarm1Maxs,alarm1Maxval =-1,0,0,1,120
            posta2, alarm2mins, alarm2minval, alarm2Maxs,alarm2Maxval = -1,0,0,1,120
            posta3, alarm3mins, alarm3minval, alarm3Maxs,alarm3Maxval = -1,0,0,1,120
            posta3, alarm4mins, alarm4minval, alarm4Maxs,alarm4Maxval = -1,0,0,1,120
            posta3, alarm5mins, alarm5minval, alarm5Maxs,alarm5Maxval = -1,0,0,1,120
            posta3, alarm1t, alarm2t, alarm3t, alarm4t, alarm5t = 'Set Alarm' 
        
        self.cfg2 = wx.Config('sensorsettings')
        self.Choices=[]
        if self.cfg2.Exists('Supported PIDs'):                         
            for i, e in enumerate(self.sensors):             
                if self.cfg2.ReadBool(e.name)==True:
                    self.Choices.append(e.name)
                    
                    
        else:
            print'empty list'
            
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText20 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )
        self.m_staticText20.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer10.Add( self.m_staticText20, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0 )
        
        self.m_staticText201 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm Name On/Off Minimum Value On/Off Maximum Value", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText201.Wrap( -1 )
        self.m_staticText201.SetFont( wx.Font( 8, 74, 90, 91, False, "Calibri Light" ) )
        
        bSizer10.Add( self.m_staticText201, 0, wx.ALIGN_RIGHT|wx.RIGHT, 35 )
        
        fgSizer1 = wx.FlexGridSizer( 0, 5, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        

        self.a1t = wx.ComboBox( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm1", wx.DefaultPosition, wx.Size( 100,-1 ),  self.Choices, 0 )
        self.a1t.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        posta1=self.a1t.FindString(alarm1t)
        self.a1t.SetSelection(posta1)
        if posta1 == -1:  self.a1t.SetValue('Set Alarm 1')
        fgSizer1.Add( self.a1t, 0, wx.ALL, 5 )
        
        self.a1am = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a1am, 0, wx.ALL, 5 )
        self.a1am.SetValue(alarm1mins) 
        
        self.a1Sm = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        fgSizer1.Add( self.a1Sm, 0, wx.ALL, 5 )
        self.a1Sm.SetValue(alarm1minval)
         
        
        self.a1aM = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a1aM, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        self.a1aM.SetValue(alarm1Maxs) 
        
        self.a1SM = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a1SM.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a1SM.SetValue(alarm1Maxval) 
        
        fgSizer1.Add( self.a1SM, 0, wx.ALL, 5 )
        
        self.a2t = wx.ComboBox( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm2", wx.DefaultPosition, wx.Size( 100,-1 ),  self.Choices, 0 )
        self.a2t.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        posta2=self.a2t.FindString(alarm2t)
        self.a2t.SetSelection(posta2)
        if posta2 == -1:  self.a2t.SetValue('Set Alarm 2')

        
        fgSizer1.Add( self.a2t, 0, wx.ALL, 5 )
        
        self.a2am = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a2am, 0, wx.ALL, 5 )
        self.a2am.SetValue(alarm2mins) 
        
        self.a2Sm = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a2Sm.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a2Sm.SetValue(alarm2minval)
        
        fgSizer1.Add( self.a2Sm, 0, wx.ALL, 5 )
        
        self.a2aM = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a2aM, 0, wx.ALL, 5 )
        self.a2aM.SetValue(alarm2Maxs) 

        self.a2SM = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a2SM.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a2SM.SetValue(alarm2Maxval) 

        fgSizer1.Add( self.a2SM, 0, wx.ALL, 5 )
        
        self.a3t = wx.ComboBox( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm3", wx.DefaultPosition, wx.Size( 100,-1 ),  self.Choices, 0 )
        self.a3t.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        posta3=self.a3t.FindString(alarm3t)
        self.a3t.SetSelection(posta3)
        if posta3 == -1:  self.a3t.SetValue('Set Alarm 3')

        fgSizer1.Add( self.a3t, 0, wx.ALL, 5 )
        
        self.a3am = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a3am, 0, wx.ALL, 5 )
        self.a3am.SetValue(alarm3mins) 
        
        self.a3Sm = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a3Sm.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a3Sm.SetValue(alarm3minval)
        
        fgSizer1.Add( self.a3Sm, 0, wx.ALL, 5 )
        
        self.a3aM = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a3aM, 0, wx.ALL, 5 )
        self.a3aM.SetValue(alarm3Maxs) 

        self.a3SM = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a3SM.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a3SM.SetValue(alarm3Maxval) 
        
        fgSizer1.Add( self.a3SM, 0, wx.ALL, 5 )
        
        self.a4t = wx.ComboBox( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm5", wx.DefaultPosition, wx.Size( 100,-1 ),  self.Choices, 0 )
        self.a4t.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        posta4=self.a4t.FindString(alarm4t)
        self.a4t.SetSelection(posta4)
        if posta4 == -1:  self.a4t.SetValue('Set Alarm 4')

        fgSizer1.Add( self.a4t, 0, wx.ALL, 5 )
        
        self.a4am = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a4am, 0, wx.ALL, 5 )
        self.a4am.SetValue(alarm4mins) 
        
        self.a4Sm = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a4Sm.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a4Sm.SetValue(alarm4minval)

        
        fgSizer1.Add( self.a4Sm, 0, wx.ALL, 5 )
        
        self.a4aM = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a4aM, 0, wx.ALL, 5 )
        self.a4aM.SetValue(alarm4Maxs) 

        self.a4SM = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 6 )
        self.a4SM.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a4SM.SetValue(alarm4Maxval) 
        
        fgSizer1.Add( self.a4SM, 0, wx.ALL, 5 )
        
        self.a5t = wx.ComboBox( self.m_scrolledWindow1, wx.ID_ANY, u"Alarm5", wx.DefaultPosition, wx.Size( 100,-1 ),  self.Choices, 0 )
        self.a5t.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        posta5=self.a5t.FindString(alarm5t)
        self.a5t.SetSelection(posta5)
        if posta5 == -1:  self.a5t.SetValue('Set Alarm 5')
        
        fgSizer1.Add( self.a5t, 0, wx.ALL, 5 )
        
        self.a5am = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a5am, 0, wx.ALL, 5 )
        self.a5am.SetValue(alarm5mins) 
        
        self.a5Sm = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 0 )
        self.a5Sm.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a5Sm.SetValue(alarm5minval)
    
        fgSizer1.Add( self.a5Sm, 0, wx.ALL, 5 )
        
        self.a5aM = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.a5aM, 0, wx.ALL, 5 )
        self.a5aM.SetValue(alarm5Maxs) 
        
        self.a5SM = wx.SpinCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 20, 6 )
        self.a5SM.SetFont( wx.Font( 8, 74, 90, 90, False, "Calibri" ) )
        self.a5SM.SetValue(alarm5Maxval) 
        
        fgSizer1.Add( self.a5SM, 0, wx.ALL, 5 )
        
        
        bSizer10.Add( fgSizer1, 1, wx.EXPAND, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.alarmsavebutton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        bSizer7.Add( self.alarmsavebutton, 0, wx.ALL, 5 )
        
        self.alarmallbutton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Disable All", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        bSizer7.Add( self.alarmallbutton, 0, wx.ALL, 5 )
        
        self.alarmdefaultbutton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Default", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        bSizer7.Add( self.alarmdefaultbutton, 0, wx.ALL, 5 )
        
               
        
        bSizer10.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        
        self.m_scrolledWindow1.SetSizer( bSizer10 )
        self.m_scrolledWindow1.Layout()
        bSizer10.Fit( self.m_scrolledWindow1 )
        bSizer2.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.alarmsavebutton.Bind( wx.EVT_BUTTON, self.OnAlarmSave )
        self.alarmallbutton.Bind( wx.EVT_BUTTON, self.OnDisableAlarmss )
        self.alarmdefaultbutton.Bind( wx.EVT_BUTTON, self.OnAlarmDefault )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    
    def OnAlarmSave( self, event ):
        alarm1t = self.a1t.GetStringSelection() 
        alarm1mins= self.a1am.Get3StateValue()
        alarm1minval = self.a1Sm.GetValue()
        alarm1Maxs= self.a1aM.Get3StateValue()
        alarm1Maxval = self.a1SM.GetValue()

        alarm2t = self.a2t.GetStringSelection()         
        alarm2mins= self.a2am.Get3StateValue()
        alarm2minval = self.a2Sm.GetValue()
        alarm2Maxs= self.a2aM.Get3StateValue()
        alarm2Maxval = self.a2SM.GetValue()
       
        alarm3t = self.a3t.GetStringSelection()        
        alarm3mins= self.a3am.Get3StateValue()
        alarm3minval = self.a3Sm.GetValue()
        alarm3Maxs= self.a3aM.Get3StateValue()
        alarm3Maxval = self.a3SM.GetValue()
        
        alarm4t = self.a4t.GetStringSelection() 
        alarm4mins= self.a4am.Get3StateValue()
        alarm4minval = self.a4Sm.GetValue()
        alarm4Maxs= self.a4aM.Get3StateValue()
        alarm4Maxval = self.a4SM.GetValue()
        
        alarm5t = self.a5t.GetStringSelection() 
        alarm5mins= self.a5am.Get3StateValue()
        alarm5minval = self.a5Sm.GetValue()
        alarm5Maxs= self.a5aM.Get3StateValue()
        alarm5Maxval = self.a5SM.GetValue()
        
        self.cfg.Write("alarm1",alarm1t)
        self.cfg.WriteInt("alarm1minstatus", alarm1mins)
        self.cfg.WriteInt("alarm1minvalue", alarm1minval)
        self.cfg.WriteInt("alarm1Maxstatus", alarm1Maxs)
        self.cfg.WriteInt("alarm1Maxvalue", alarm1Maxval)

        self.cfg.Write("alarm2",alarm2t)
        self.cfg.WriteInt("alarm2minstatus", alarm2mins)
        self.cfg.WriteInt("alarm2minvalue", alarm2minval)
        self.cfg.WriteInt("alarm2Maxstatus", alarm2Maxs)
        self.cfg.WriteInt("alarm2Maxvalue", alarm2Maxval)
        
        self.cfg.Write("alarm3",alarm3t)
        self.cfg.WriteInt("alarm3minstatus", alarm3mins)
        self.cfg.WriteInt("alarm3minvalue", alarm3minval)
        self.cfg.WriteInt("alarm3Maxstatus", alarm3Maxs)
        self.cfg.WriteInt("alarm3Maxvalue", alarm3Maxval)
        
        self.cfg.Write("alarm4",alarm4t)
        self.cfg.WriteInt("alarm4minstatus", alarm4mins)
        self.cfg.WriteInt("alarm4minvalue", alarm4minval)
        self.cfg.WriteInt("alarm4Maxstatus", alarm4Maxs)
        self.cfg.WriteInt("alarm4Maxvalue", alarm4Maxval)
        
        self.cfg.Write("alarm5",alarm5t)
        self.cfg.WriteInt("alarm5minstatus", alarm5mins)
        self.cfg.WriteInt("alarm5minvalue", alarm5minval)
        self.cfg.WriteInt("alarm5Maxstatus", alarm5Maxs)
        self.cfg.WriteInt("alarm5Maxvalue", alarm5Maxval)
        
        #self.statusBar.SetStatusText('Configuration saved, %s ' % wx.Now())

        
    
    def OnDisableAlarmss( self, event ):
        self.a1t.SetValue('Set Alarm 1')
        self.a1am.SetValue(False)
        self.a1aM.SetValue(False)
        self.a2t.SetValue('Set Alarm 2')
        self.a2am.SetValue(False)
        self.a2aM.SetValue(False)
        self.a3am.SetValue(False)
        self.a3aM.SetValue(False)
        self.a4am.SetValue(False)
        self.a4aM.SetValue(False)
        self.a5am.SetValue(False)
        self.a5aM.SetValue(False)
        
 
    
    def OnAlarmDefault( self, event ):
        self.a1t.SetValue('Set Alarm 1')
        self.a1am.SetValue(False) 
        self.a1Sm.SetValue(0) 
        self.a1aM.SetValue(False)  
        self.a1SM.SetValue(0)
        
        self.a2t.SetValue('Set Alarm 2')
        self.a2am.SetValue(False) 
        self.a2Sm.SetValue(0) 
        self.a2aM.SetValue(False)  
        self.a2SM.SetValue(0)
        
        self.a3t.SetValue('Set Alarm 3')
        self.a3am.SetValue(False) 
        self.a3Sm.SetValue(0) 
        self.a3aM.SetValue(False)  
        self.a3SM.SetValue(0)
        
        self.a4t.SetValue('Set Alarm 4')
        self.a4am.SetValue(False) 
        self.a4Sm.SetValue(0) 
        self.a4aM.SetValue(False)  
        self.a4SM.SetValue(0)
        
        self.a5t.SetValue('Set Alarm 5')
        self.a5am.SetValue(False) 
        self.a5Sm.SetValue(0) 
        self.a5aM.SetValue(False)  
        self.a5SM.SetValue(0)
        
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def setPort(self, port):
        self.port = port
        
    def getSensors(self):
        return self.sensors
        
    def getPort(self):
        return self.port               
    
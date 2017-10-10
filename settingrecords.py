#SELECTOR MULTIPLE
import sys

from pylab import plotfile, show, gca
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

import matplotlib.cbook as cbook
import obd_sensors


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
      
class SettingRecordPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(SettingRecordPanel, self).__init__(*args, **kwargs)

        
    def showSettingRecordPanel(self):    
                   
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        panelSettings = wx.Panel( self, -1 )
   
        vboxSettings = wx.BoxSizer(wx.VERTICAL)
        hboxSettings = wx.BoxSizer(wx.HORIZONTAL)
        
        leftPanel = wx.Panel(panelSettings, -1)
        rightPanel = wx.Panel(panelSettings, -1) 
 
 
        #self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = CheckListCtrl(rightPanel)
        self.list.InsertColumn(0, 'Name', width=140)
        self.list.InsertColumn(1, 'Command')
        self.list.InsertColumn(2, 'Units')
            
        for i,e in enumerate(obd_sensors.SENSORS):
            index = self.list.InsertStringItem(sys.maxint, e.name)
            self.list.SetStringItem(index, 1, e.cmd)
            self.list.SetStringItem(index, 2, e.unit)
        
        num = self.list.GetItemCount() 
        self.cfg = wx.Config('recordsettings')
        num = self.list.GetItemCount()
        sensorlist = []
        for i in range(num):
            sensorlist.append(False)
        if self.cfg.Exists('Supported PIDs'):                     
            for i in range(num):
                self.list.CheckItem(i,self.cfg.ReadBool(self.list.GetItemText(i)))  
                                        
        else:
            for i in range(num):
                self.list.CheckItem(i,False)
                #print('Sensor ' + self.list.GetItemText(i) + ' value'+ str(self.cfg.ReadBool('Sensorlist'+str(i)))) 
        valuetoggle= False
        if self.cfg.Exists('RecordMode'):
            valuetoggle= self.cfg.ReadBool('RecordMode')    
            
        else: print 'record mode config not found'
     
        vbox2Settings = wx.BoxSizer(wx.VERTICAL)
 
        selectall = wx.Button(leftPanel, -1, 'Select All', size=(65, -1))
        deselect = wx.Button(leftPanel, -1, 'Deselect All', size=(65, -1))
        save = wx.Button(leftPanel, -1, 'Save', size=(65, -1))
        self.recrd= wx.ToggleButton(leftPanel, -1, 'Record', size=(65,-1))
        self.recrd.SetValue(valuetoggle)
        # back= wx.Button(leftPanel, -1, 'Back', size=(65,-1))
      
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=selectall.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=deselect.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=save.GetId())
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnActivate, id=self.recrd.GetId())
       
              
                   
        vbox2Settings.Add(selectall, wx.EXPAND)
        vbox2Settings.Add(deselect, wx.EXPAND)
        vbox2Settings.Add(save, wx.EXPAND)
        vbox2Settings.Add(self.recrd, wx.EXPAND)
        
        
        
        vbox = wx.BoxSizer( wx.VERTICAL )      
        vbox.Add(self.list, 1,  wx.TOP, 5)
        vbox.Add((-1, 1))
        vbox.Add((-1, 1))
          
        rightPanel.SetSizer(vbox)

        
        hboxSettings.Layout()
        vboxSettings.Layout()
        vbox2Settings.Layout()
        
        hboxSettings.Add(leftPanel, 0,  wx.RIGHT, 5) 
        hboxSettings.Add(rightPanel, 0, wx.EXPAND )
         
         
        leftPanel.SetSizer(vbox2Settings)
        panelSettings.SetSizer(hboxSettings)
        
        bSizer2.Add( panelSettings, 1, wx.EXPAND |wx.ALL, 0 )
                
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )    
         

    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)
 
    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)
 
    def OnSave(self, event):
        num = self.list.GetItemCount() 
        sensorlist = []
        self.cfg.WriteBool("Recordlist", False)
        for i in range(num):
            sensorlist.append(False)
        for i in range(num):            
            if self.list.IsChecked(i):
                self.cfg.WriteBool(self.list.GetItemText(i), True)
                #print ("guardado: sensorlist " + self.list.GetItemText(i)+ "True")
            else:
                self.cfg.WriteBool(self.list.GetItemText(i), False)    
                #print ("guardado: sensorlist " + self.list.GetItemText(i)+ "False")
            
    def OnActivate(self,event):      
        if (self.recrd.GetValue()):  self.cfg.WriteBool("RecordMode", True) 
        else: self.cfg.WriteBool("RecordMode", False) 

             
    def OnClose(self, e):          
        self.Close(True)   
 
    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def changeIntroPanel( self, event ):
        event.Skip()


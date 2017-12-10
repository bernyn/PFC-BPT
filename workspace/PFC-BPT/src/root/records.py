
#SELECTOR MULTIPLE
from _codecs import decode
from encodings import ascii
import os
import sys

from pandas.io.pytables import IndexCol
from pylab import plotfile, show, gca
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
import obd_sensors
import pandas as pd


wildcard = "log source (*.txt; *.csv; *.log)|*.txt;*.csv;*.log;|" \
         "All files (*.*)|*.*"
 
class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
      
class RecordsPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        #config values
        super(RecordsPanel, self).__init__(*args, **kwargs)

        
    def showRecordsPanel(self):    
                   
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        panelSettings = wx.Panel( self, -1 )
   
        vboxSettings = wx.BoxSizer(wx.VERTICAL)
        hboxSettings = wx.BoxSizer(wx.HORIZONTAL)
        
        leftPanel = wx.Panel(panelSettings, -1)
        rightPanel = wx.Panel(panelSettings, -1) 
 
        vbox = wx.BoxSizer(wx.VERTICAL) 
        recordbox = wx.StaticBox(rightPanel, 1, 'Records File:') 
        recordboxsSizer = wx.StaticBoxSizer(recordbox, wx.VERTICAL) 
       
        recordboxsizer = wx.BoxSizer(wx.HORIZONTAL) 
        fn = wx.StaticText(rightPanel, 1, "File:") 
        
        recordboxsizer.Add(fn, 0, wx.ALL|wx.CENTER, 1) 
        self.folderfile = wx.TextCtrl(rightPanel, -1, style = wx.ALIGN_LEFT)    
        recordboxsizer.Add(self.folderfile, 0, wx.ALL|wx.CENTER, 1)
        recordboxsSizer.Add(recordboxsizer, 0, wx.ALL|wx.CENTER, 1)  
        
        vbox.Add(recordboxsSizer,0, wx.ALL|wx.CENTER, -1)
        
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
        
     
        vbox2Settings = wx.BoxSizer(wx.VERTICAL)
 
        openfile = wx.Button(leftPanel, -1, 'Open File', size=(75, -1))
        plotrecords= wx.Button(leftPanel, -1, 'Plot records', size=(75, -1))
        selectall = wx.Button(leftPanel, -1, 'Select All', size=(75, -1))
        deselect = wx.Button(leftPanel, -1, 'Deselect All', size=(75, -1))
        recordinfo = wx.Button(leftPanel, -1, 'Record info', size=(75, -1))
        deletefile = wx.Button(leftPanel, -1, 'Delete File', size=(75, -1))

        self.Bind(wx.EVT_BUTTON, self.OnOpen, id=openfile.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnPlot, id=plotrecords.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=selectall.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=deselect.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRecordInfo, id=recordinfo.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeleteFile, id=deletefile.GetId())
                         
        vbox2Settings.Add(openfile, wx.EXPAND)
        vbox2Settings.Add(plotrecords, wx.EXPAND)        
        vbox2Settings.Add(selectall, wx.EXPAND)
        vbox2Settings.Add(deselect, wx.EXPAND)
        vbox2Settings.Add(recordinfo, wx.EXPAND)
        vbox2Settings.Add(deletefile, wx.EXPAND)
                
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
         
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def OnOpen(self,event):
        print 'openfile'
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for self.path in self.paths:
                print self.path
            self.folderfile.SetValue(self.path)
        
        dlg.Destroy()  
        
    def OnPlot(self,event):       
        if self.folderfile.IsEmpty()==False:
            data = pd.read_csv(self.path, sep=';',index_col= 'time', parse_dates=True)
            num = self.list.GetItemCount()
            toplot=[]           
            index=1
            for i in range(num):            
                if self.list.IsChecked(i):
                    toplot.insert(index,self.list.GetItemText(i))
                    index=+1
            toplot = [x.encode('utf-8') for x in toplot]
            
            datatoplot = data[toplot]
            datatoplot.plot()
            show() 
            

        else: wx.MessageBox("No Record File selected","Warning",wx.OK)
     
        
    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)
 
    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)
 
     
    def OnDeleteFile(self,event):
        if self.folderfile.IsEmpty()==False:
            if wx.MessageBox("Are You Sure you want to delete the file "+self.folderfile.GetValue()+" ?","Delete File",wx.YES_NO) == wx.YES:
                os.remove(self.path)
                self.folderfile.Clear()
            else:
                print ("User did not click yes (clicked No or closed)")
        else: wx.MessageBox("No Record File selected","Warning",wx.OK)
    
    def OnRecordInfo(self,event):
        if self.folderfile.IsEmpty()==False:
            data = pd.read_csv(self.path, sep=';',parse_dates=True)
            num = self.list.GetItemCount()
            toplot=[]
            index=0
            for i in range(num):            
                if self.list.IsChecked(i):
                    toplot.insert(index,self.list.GetItemText(i))
                    index+=1
                    
            toplot = [x.encode('utf-8') for x in toplot]
            
            print index
            if index > 7: #check if 0
                wx.MessageBox("Please choose 6 sensor max","Warning",wx.OK)
            else:    
                wx.MessageBox(str(data[toplot].agg([np.max, np.min, np.mean, np.std, len])),'Record Info' ,wx.OK) 
        else: wx.MessageBox("No Record File selected","Warning",wx.OK)
                  
            
    def OnClose(self, e):          
        self.Close(True)   
 
    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def changeIntroPanel( self, event ):
        event.Skip()
    
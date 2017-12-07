# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from math import pi, sqrt
from modenumerical import PopupUP

import wx

import obd_sensors
import wx.grid as gridlib
import wx.lib.agw.speedmeter as SM


###########################################################################
## Class frameGraphical
###########################################################################
class ModeGraphicalPanel ( wx.Panel ):
    
        
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeGraphicalPanel, self).__init__(*args, **kwargs)
         # Connection
        self.connection = None

        # Sensors 
        self.istart = 0
        self.sensors = []
        
        # Port 
        self.port = None
        
        self.rpm = 0
        self.speed = 0
        self.ecomode = False
        
        self.cfg = wx.Config('sensorsettings')
        num = enumerate(obd_sensors.SENSORS) 
        sensorlist = []
        
        if self.cfg.Exists('Supported PIDs'):             
            self.displayKmh = self.cfg.ReadBool('           Vehicle Speed')
            self.displayRPM = self.cfg.ReadBool('              Engine RPM')
            self.displayCoolant = self.cfg.ReadBool('     Coolant Temp')
            self.displayIntake = self.cfg.ReadBool('         Intake Air Temp')
            self.displayLoad = self.cfg.ReadBool('   Calculated Load Value')
            self.displayMAF = self.cfg.ReadBool('     Air Flow Rate (MAF)')
                    
           
                                             
        else:
            for i in enumerate(num):
                print "no config"
        
    def setEcoMode (self,eco):
        return self.ecomode
    
    def setConnection(self, connection):
        self.connection = connection
    
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def setPort(self, port):
        self.port = port
    
    def getSensors(self):
        return self.sensors
    
    def getPort(self):
        return self.port
    
    def getSensorsToDisplay(self, istart):
        """
        Get at most 1 sensor to be displayed on screen.
        """
        sensors_display = []
        if istart<len(self.sensors):
            iend = istart + 1
            sensors_display = self.sensors[istart:iend]
        return sensors_display
    
    def showGraphicalPanel(self):            
                 

                #===============================================================
                # self.list.CheckItem(i,False)
                #===============================================================
        
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Graphical mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 74, 90, 92, False, "Calibri" ) )
        
        bSizer9.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 1 )
              
        panelGraphical = wx.Panel( self, -1 )
        sizerGraphical = wx.FlexGridSizer( 2, 3, 0, 0 )       
        
        if self.displayKmh: 
            print 'kmj'
            self.panelkmh = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)              #1 kmh
            self.addDisplayKmh(self, self.panelkmh)
        
        if self.displayRPM:
            print 'rpm'
            self.panelrpm = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)              #2 RPM
            self.addDisplayRPM(self, self.panelrpm)
        
        if self.displayCoolant:
            print 'coolant'
            self.panelcoolanttemp = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)          #3 coolanttemp
            self.addDisplayCoolant(self, self.panelcoolanttemp)
        
        if self.displayLoad:
            print 'load'
            self.panelload = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)        #4 load
            self.addDisplayLoad(self, self.panelload)
        
        if self.displayIntake:
            print 'intake'
            self.panelintaketemp = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)       #5 intaketemp
            self.addDisplayIntake(self, self.panelintaketemp)
        
        if self.displayMAF: 
            print 'maf'
            self.panelmaf = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)          #6 Maf
            self.addDisplayMAF(self, self.panelmaf)
                    

        if self.displayKmh: 
            bsizerkmh = wx.BoxSizer(wx.VERTICAL)
            hsizerkmh = wx.BoxSizer(wx.HORIZONTAL)   
            bsizerkmh.Add(self.GageKmh, 1, wx.EXPAND) 
            stattextkmh = wx.StaticText(self.panelkmh, -1, "Km/h", style=wx.ALIGN_CENTER)     
            stattextkmh.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
            hsizerkmh.Add(stattextkmh, 1, wx.EXPAND)
            bsizerkmh.Add(hsizerkmh, 0, wx.EXPAND)
            self.panelkmh.SetSizer(bsizerkmh)
        
        if self.displayRPM:
            bsizerrpm = wx.BoxSizer(wx.VERTICAL)
            hsizerrpm = wx.BoxSizer(wx.HORIZONTAL)
            bsizerrpm.Add(self.GageRPM, 1, wx.EXPAND) 
            stattextrpm = wx.StaticText(self.panelrpm, -1, "RPM x 100", style=wx.ALIGN_CENTER)
            stattextrpm.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
            hsizerrpm.Add(stattextrpm, 1, wx.EXPAND)       
            bsizerrpm.Add(hsizerrpm, 0, wx.EXPAND)       
            self.panelrpm.SetSizer(bsizerrpm)
            
        
        if self.displayCoolant:
            bsizercoolanttemp = wx.BoxSizer(wx.VERTICAL)        
            hsizercoolanttemp = wx.BoxSizer(wx.HORIZONTAL)                
            bsizercoolanttemp.Add(self.GageCoolantTemp, 1, wx.EXPAND)
            stattextcoolanttemp = wx.StaticText(self.panelcoolanttemp, -1, "Coolant Temp", style=wx.ALIGN_CENTER)
            stattextcoolanttemp.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
            hsizercoolanttemp.Add(stattextcoolanttemp, 1, wx.EXPAND)
            bsizercoolanttemp.Add(hsizercoolanttemp, 0, wx.EXPAND)
            self.panelcoolanttemp.SetSizer(bsizercoolanttemp)
                 
        
        if self.displayLoad:
            bsizerload = wx.BoxSizer(wx.VERTICAL)
            hsizerload = wx.BoxSizer(wx.HORIZONTAL)                      
            bsizerload.Add(self.GageLoad, 1, wx.EXPAND)
            stattextload = wx.StaticText(self.panelload, -1, "Load", style=wx.ALIGN_CENTER)
            stattextload.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
            hsizerload.Add(stattextload, 1, wx.EXPAND)
            bsizerload.Add(hsizerload, 0, wx.EXPAND)
            self.panelload.SetSizer(bsizerload)
        
        if self.displayIntake:
            bsizerintaketemp = wx.BoxSizer(wx.VERTICAL)
            hsizerintaketemp = wx.BoxSizer(wx.HORIZONTAL)                    
            bsizerintaketemp.Add(self.GageIntakeTemp, 1, wx.EXPAND)
            stattextintaketemp= wx.StaticText(self.panelintaketemp, -1, "Intake Temp", style=wx.ALIGN_CENTER)
            stattextintaketemp.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
            hsizerintaketemp.Add(stattextintaketemp, 1, wx.EXPAND)
            bsizerintaketemp.Add(hsizerintaketemp, 0, wx.EXPAND)
            self.panelintaketemp.SetSizer(bsizerintaketemp)        
        
        if self.displayMAF:                   
            bsizermaf = wx.BoxSizer(wx.VERTICAL)
            hsizermaf = wx.BoxSizer(wx.HORIZONTAL)
            bsizermaf.Add(self.GageMAF, 1, wx.EXPAND)
            stattextmaf = wx.StaticText(self.panelmaf, -1, "MAF", style=wx.ALIGN_CENTER)
            stattextmaf.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
            hsizermaf.Add(stattextmaf, 1, wx.EXPAND)
            bsizermaf.Add(hsizermaf, 0, wx.EXPAND)
            self.panelmaf.SetSizer(bsizermaf)
        
        
        if self.displayKmh: sizerGraphical.Add(self.panelkmh,  1, wx.EXPAND)
        if self.displayRPM: sizerGraphical.Add(self.panelrpm,  1, wx.EXPAND)
        if self.displayLoad: sizerGraphical.Add(self.panelairtemp,  1, wx.EXPAND) 
        if self.displayCoolant: sizerGraphical.Add(self.panelblocktemp, 1, wx.EXPAND) 
        if self.displayIntake: sizerGraphical.Add(self.panelintaketemp, 1, wx.EXPAND)  
        if self.displayMAF: sizerGraphical.Add(self.paneloiltemp,  1, wx.EXPAND) 

        sizerGraphical.AddGrowableRow(0)
        sizerGraphical.AddGrowableRow(1)
        
        sizerGraphical.AddGrowableCol(0)
        sizerGraphical.AddGrowableCol(1)
        sizerGraphical.AddGrowableCol(2)
        
        panelGraphical.SetSizer(sizerGraphical)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(panelGraphical, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        mainSizer.Layout()

         # Handle events for mouse clicks
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeft)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRight)
    
    def  addDisplayKmh(self, event,panelkmh):  
        # Panel 1 Km/h SpeedMeter        
        self.GageKmh = SM.SpeedMeter(panelkmh,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_ROTATE_TEXT
                                
                                          )
                                
        self.GageKmh.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(0, 201, 20)
        self.GageKmh.SetIntervals(intervals)
        colours = [wx.BLACK]*10
        self.GageKmh.SetIntervalColours(colours)
        ticks = [str(interval) for interval in intervals]
        self.GageKmh.SetTicks(ticks)
        self.GageKmh.SetTicksColour(wx.WHITE)
        self.GageKmh.SetTicksFont( wx.Font( 4, 74, 90, 90, False, "Calibri" ) )   
        self.GageKmh.SetNumberOfSecondaryTicks(2)
        self.GageKmh.SetHandColour(wx.Colour(255, 50, 0))      
        self.GageKmh.SetSpeedBackground(wx.BLACK)        
        self.GageKmh.SetHandColour(wx.WHITE)
        self.GageKmh.DrawExternalArc(False)
        self.GageKmh.SetSpeedValue(5.6)
    
    def  addDisplayRPM(self, event,panelrpm):
        # Panel 2 RPM
        self.GageRPM = SM.SpeedMeter(panelrpm,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_PARTIAL_FILLER |
                                          SM.SM_ROTATE_TEXT
                                
                                          )
                                
        self.GageRPM.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(0, 61, 10)
        self.GageRPM.SetIntervals(intervals)
        colours = [wx.BLACK]*4
        colours.append(wx.Colour(128, 128, 128))
        colours.append(wx.RED)
        self.GageRPM.SetIntervalColours(colours)
        ticks = [str(interval) for interval in intervals]
        self.GageRPM.SetTicks(ticks)
        self.GageRPM.SetTicksColour(wx.WHITE)
        self.GageRPM.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )      
        self.GageRPM.SetNumberOfSecondaryTicks(4)
        self.GageRPM.SetHandColour(wx.Colour(255, 50, 0))      
        self.GageRPM.SetArcColour(wx.BLUE)
        self.GageRPM.SetSpeedBackground(wx.BLACK)        
        self.GageRPM.SetHandColour(wx.WHITE)
        self.GageRPM.DrawExternalArc(False)
        self.GageRPM.SetSpeedValue(5.6)
    
    
    def  addDisplayCoolant(self, event,panelcoolanttemp): 
        # Panel 3 Coolant Temp
        self.GageCoolantTemp = SM.SpeedMeter(panelcoolanttemp,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_MIDDLE_ICON,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )
        self.GageCoolantTemp.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(-5, 46, 5)
        self.GageCoolantTemp.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*7)
        colours.append(wx.RED)
        self.GageCoolantTemp.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageCoolantTemp.SetTicks(ticks)
        self.GageCoolantTemp.SetTicksColour(wx.WHITE)
        self.GageCoolantTemp.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )      
        self.GageCoolantTemp.SetHandColour(wx.WHITE)
        self.GageCoolantTemp.SetSpeedBackground(wx.BLACK)        
        self.GageCoolantTemp.DrawExternalArc(False)
        self.GageCoolantTemp.SetHandColour(wx.WHITE)
        self.GageCoolantTemp.SetShadowColour(wx.Colour(50, 50, 50))               
        self.GageCoolantTemp.SetSpeedValue(40)
    
    def  addDisplayLoad(self, event,panelload):
        # Pabek 4 LOAD     
        self.GageLoad = SM.SpeedMeter(panelload,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )       
        self.GageLoad.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(20, 100, 10)
        self.GageLoad.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*7)
        colours.append(wx.RED)
        self.GageLoad.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageLoad.SetTicks(ticks)
        self.GageLoad.SetTicksColour(wx.WHITE)
        self.GageLoad.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" )  )       
        self.GageLoad.SetHandColour(wx.WHITE)
        self.GageLoad.SetSpeedBackground(wx.BLACK)        
        self.GageLoad.DrawExternalArc(False)
        self.GageLoad.SetHandColour(wx.WHITE)               
        self.GageLoad.SetSpeedValue(40)
    
    def  addDisplayIntake(self, event,panelintaketemp):
        # Panel 5 Intake Temp
        self.GageIntakeTemp = SM.SpeedMeter(panelintaketemp,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS ,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )

        self.GageIntakeTemp.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(0, 81, 10)
        self.GageIntakeTemp.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*5)
        colours.append(wx.RED)

        self.GageIntakeTemp.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageIntakeTemp.SetTicks(ticks)
        self.GageIntakeTemp.SetTicksColour(wx.WHITE)
        self.GageIntakeTemp.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )
        self.GageIntakeTemp.SetSpeedBackground(wx.BLACK)
        self.GageIntakeTemp.DrawExternalArc(False)
        self.GageIntakeTemp.SetHandColour(wx.WHITE)    
        # Quite An High Fever!!!        
        self.GageIntakeTemp.SetSpeedValue(80)  
    
    def  addDisplayMAF(self, event,panelmaf):
                # Panel 6 MAF
        self.GageMAF = SM.SpeedMeter(panelmaf,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )

        self.GageMAF.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(20, 101, 10)
        self.GageMAF.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*7)
        colours.append(wx.RED)
        self.GageMAF.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageMAF.SetTicks(ticks)
        self.GageMAF.SetTicksColour(wx.WHITE)
        self.GageMAF.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )       
        self.GageMAF.SetHandColour(wx.WHITE)
        self.GageMAF.SetSpeedBackground(wx.BLACK)
        self.GageMAF.SetArcColour(wx.BLUE)
        self.GageMAF.DrawExternalArc(False)
        self.GageMAF.SetHandColour(wx.WHITE)       
        self.GageMAF.SetSpeedValue(40)
    
    def ShowSensors(self):
        
        sensors = self.getSensorsToDisplay(self.istart)
        
        for index, sensor in sensors:
        
            if self.displayKmh & index ==13:
                print 'get kmh'
                (name, value, unit) = self.port.sensor(index)
                self.GageKmh.SetSpeedValue(value)    
                 
            if self.displayRPM & index ==12:
                print 'get rpm'
                (name, value, unit) = self.port.sensor(index) 
                self.GageRPM.SetSpeedValue(value)
                   
            if self.displayLoad & index ==4:
               print 'get load'
               (name, value, unit) = self.port.sensor(index)  
               self.GageLoad.SetSpeedValue(value)
                     
            if self.displayCoolant & index ==5:
                print 'get coolant'
                (name, value, unit) = self.port.sensor(index)
                self.GageCoolantTemp.SetSpeedValue(value) 
                    
            if self.displayIntake & index ==15:
                print 'get intake'
                (name, value, unit) = self.port.sensor(index) 
                self.GageIntakeTemp.SetSpeedValue(value)
                                  
            if self.displayMAF & index ==16:
                print 'get maf'  
                (name, value, unit) = self.port.sensor(index) 
                self.GageMAF.SetSpeedValue(value)   
                   
                    
        # Timer for update
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)
        self.timer.Start(1000)


    def refresh(self, event):
        sensors = self.getSensorsToDisplay(self.istart)
        print 'refresh'
        for index, sensor in sensors:
            print index
            print sensor
         
            if self.displayKmh & index ==13:
                print 'get kmh'
                (name, value, unit) = self.port.sensor(index)
                self.GageKmh.SetSpeedValue(value)
                print name
                print str(value)
                print (unit)    
                 
            if self.displayRPM & index ==12:
                print 'get rpm'
                (name, value, unit) = self.port.sensor(index) 
                self.GageRPM.SetSpeedValue(value)
                print name
                print str(value)
                print (unit)
                   
            if self.displayLoad & index ==4:
               print 'get load'
               (name, value, unit) = self.port.sensor(index)  
               self.GageLoad.SetSpeedValue(value)
               print name
               print str(value)
               print (unit)
                     
            if self.displayCoolant & index ==5:
                print 'get coolant'
                (name, value, unit) = self.port.sensor(index)
                self.GageCoolantTemp.SetSpeedValue(value) 
                print name
                print str(value)
                print (unit)     
            if self.displayIntake & index ==15:
                print 'get intake'
                (name, value, unit) = self.port.sensor(index) 
                self.GageIntakeTemp.SetSpeedValue(value)
                print name
                print str(value)
                print (unit)                  
            if self.displayMAF & index ==16:
                print 'get maf'  
                (name, value, unit) = self.port.sensor(index) 
                self.GageMAF.SetSpeedValue(value)   
                print name
                print str(value)
                print (unit)
    def onCtrlC(self, event):
        self.GetParent().Close()  
    
    def onLeft(self, event):
        """
        Get data from 1 previous sensor in the list.
        """
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
        istart = self.istart + 1
        if istart<len(self.sensors):
            self.istart = istart
            self.ShowSensors()
        else: 
            istart = self.istart - 31 
            self.istart = istart 
            self.ShowSensors()  
    
    def __del__( self ):
        pass
    

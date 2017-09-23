# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import wx
import wx.grid as gridlib
import wx.lib.agw.speedmeter as SM
from math import pi, sqrt
import obd_sensors



###########################################################################
## Class frameGraphical
###########################################################################

class ModeGraphicalPanel ( wx.Panel ):
    
        
    def __init__(self, *args, **kwargs):
        #config values
        super(ModeGraphicalPanel, self).__init__(*args, **kwargs)

    def showGraphicalPanel(self):            
        #=======================================================================
        # num = self.list.GetItemCount() 
        # self.cfg = wx.Config('sensorsettings')
        # num = self.list.GetItemCount()
        # sensorlist = []
        # for i in range(num):
        #     sensorlist.append(False)
        # if self.cfg.Exists('Supported PIDs'):             
        #    # print ("confg load")
        #     for i in range(num):
        #         self.list.CheckItem(i,self.cfg.ReadBool(self.list.GetItemText(i)))  
        #         #print('Sensor ' + self.list.GetItemText(i) + ' value'+ str(self.cfg.ReadBool('Sensorlist'+str(i))))                        
        # else:
        #     for i in range(num):
        #         self.list.CheckItem(i,False)
        #         #print('Sensor ' + self.list.GetItemText(i) + ' value'+ str(self.cfg.ReadBool('Sensorlist'+str(i)))) 
        #=======================================================================
        
              
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
            
        self.cfg = wx.Config('sensorsettings')
        num = enumerate(obd_sensors.SENSORS) 
        sensorlist = []
        
        if self.cfg.Exists('Supported PIDs'):             
            #===================================================================
            # i= 4  Calculated Load Value value= True
            # i= 5  Coolant Temperature value= True
            # i= 1  Engine RPM value= True
            # i= 13 Vehicle Speed value= True
            # i= 15 Intake Air Temp value= True
            # i= 16 Air Flow Rate (MAF) value= True
            #===================================================================
            displayKmh = self.cfg.ReadBool('           Vehicle Speed')
            displayRPM = self.cfg.ReadBool('              Engine RPM')
            displayCoolant = self.cfg.ReadBool('     Coolant Temperature')
            displayIntake = self.cfg.ReadBool('         Intake Air Temp')
            displayLoad = self.cfg.ReadBool('   Calculated Load Value')
            displayMAF = self.cfg.ReadBool('     Air Flow Rate (MAF)')
                    
           
                                             
        else:
            for i in range(num):
                print "no config"
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
        
        panelkmh = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)              #1 kmh
        panelrpm = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)              #2 RPM
        panelairtemp = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)          #3 airtemp
        panelblocktemp = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)        #4 BlockTemp
        panelintaketemp = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)       #5 intaketemp
        paneloiltemp = wx.Panel(panelGraphical, -1, style=wx.RAISED_BORDER)          #6 oiltemp
        
        # Panel 1 Km/h SpeedMeter        
        self.GageKmh = SM.SpeedMeter(panelkmh,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          #SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          #SM.SM_DRAW_MIDDLE_TEXT |
                                          #SM.SM_DRAW_PARTIAL_FILLER |
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
        #=======================================================================
        # self.GageKmh.SetMiddleText("Km/h")
        # self.GageKmh.SetMiddleTextColour(wx.WHITE)
        # self.GageKmh.SetMiddleTextFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )
        #=======================================================================
        self.GageKmh.SetSpeedValue(5.6)
      
       
        # Panel 2 RPM
       
        self.GageRPM = SM.SpeedMeter(panelrpm,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          #SM.SM_DRAW_MIDDLE_TEXT |
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
        #=======================================================================
        # self.GageRPM.SetMiddleText("RPM x 100")
        # self.GageRPM.SetMiddleTextColour(wx.WHITE)
        # self.GageRPM.SetMiddleTextFont( wx.Font( 86, 74, 90, 90, False, "Calibri" ) )
        #=======================================================================
        self.GageRPM.SetSpeedValue(5.6)
       
      
        # Panel 3 Air Temp
        
        self.GageAirTemp = SM.SpeedMeter(panelairtemp,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          #SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_DRAW_MIDDLE_ICON,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )
        self.GageAirTemp.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(-5, 46, 5)
        self.GageAirTemp.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*7)
        colours.append(wx.RED)
        self.GageAirTemp.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageAirTemp.SetTicks(ticks)
        self.GageAirTemp.SetTicksColour(wx.WHITE)
        self.GageAirTemp.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )      
        self.GageAirTemp.SetHandColour(wx.WHITE)
        self.GageAirTemp.SetSpeedBackground(wx.BLACK)        
        #=======================================================================
        # self.GageAirTemp.SetMiddleText("AIR c")
        # self.GageAirTemp.SetMiddleTextColour(wx.WHITE)
        # self.GageAirTemp.SetMiddleTextFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )
        #=======================================================================
        self.GageAirTemp.DrawExternalArc(False)
        self.GageAirTemp.SetHandColour(wx.WHITE)
        self.GageAirTemp.SetShadowColour(wx.Colour(50, 50, 50))               
        self.GageAirTemp.SetSpeedValue(40)
      
        # Pabek 4 Block Temp     
        self.GageBlockTemp = SM.SpeedMeter(panelblocktemp,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS,
                                          #SM.SM_DRAW_MIDDLE_TEXT |
                                          #SM.SM_DRAW_MIDDLE_ICON,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )

        
        self.GageBlockTemp.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(20, 121, 10)
        self.GageBlockTemp.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*7)
        colours.append(wx.RED)
        self.GageBlockTemp.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageBlockTemp.SetTicks(ticks)
        self.GageBlockTemp.SetTicksColour(wx.WHITE)
        self.GageBlockTemp.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" )  )       
        self.GageBlockTemp.SetHandColour(wx.WHITE)
        self.GageBlockTemp.SetSpeedBackground(wx.BLACK)        
        #=======================================================================
        # self.GageBlockTemp.SetMiddleText("BLOCK c")
        # self.GageBlockTemp.SetMiddleTextColour(wx.WHITE)
        # self.GageBlockTemp.SetMiddleTextFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD))
        #=======================================================================
        self.GageBlockTemp.DrawExternalArc(False)
        self.GageBlockTemp.SetHandColour(wx.WHITE)               
        self.GageBlockTemp.SetSpeedValue(40)
                       
        # Panel 5 Intake Temp
        self.GageIntakeTemp = SM.SpeedMeter(panelintaketemp,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS ,
                                          #SM.SM_DRAW_MIDDLE_TEXT |
                                          #SM.SM_DRAW_MIDDLE_ICON,
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
        #=======================================================================
        # self.GageIntakeTemp.SetMiddleText("INTAKE c ")
        # self.GageIntakeTemp.SetMiddleTextColour(wx.WHITE)
        # self.GageIntakeTemp.SetMiddleTextFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD))
        # self.GageIntakeTemp.SetHandColour(wx.WHITE)
        #=======================================================================
        #Set The Background Color Of The GageIntaketemp OutSide The Control
        self.GageIntakeTemp.SetSpeedBackground(wx.BLACK)
        self.GageIntakeTemp.DrawExternalArc(False)
        self.GageIntakeTemp.SetHandColour(wx.WHITE)    
        # Quite An High Fever!!!        
        self.GageIntakeTemp.SetSpeedValue(80)


        # Panel 6 Oil Temp
        
        self.GageOilTemp = SM.SpeedMeter(paneloiltemp,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS,
                                          #SM.SM_DRAW_MIDDLE_TEXT |
                                          #SM.SM_DRAW_MIDDLE_ICON,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )

        self.GageOilTemp.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(20, 121, 10)
        self.GageOilTemp.SetIntervals(intervals)
        colours = [wx.BLUE]*2
        colours.extend([wx.BLACK]*7)
        colours.append(wx.RED)
        self.GageOilTemp.SetIntervalColours(colours)
        ticks = [str(interval) + "c" for interval in intervals]
        self.GageOilTemp.SetTicks(ticks)
        self.GageOilTemp.SetTicksColour(wx.WHITE)
        self.GageOilTemp.SetTicksFont( wx.Font( 6, 74, 90, 90, False, "Calibri" ) )       
        self.GageOilTemp.SetHandColour(wx.WHITE)
        self.GageOilTemp.SetSpeedBackground(wx.BLACK)
        self.GageOilTemp.SetArcColour(wx.BLUE)
        self.GageOilTemp.DrawExternalArc(False)
        self.GageOilTemp.SetHandColour(wx.WHITE)
        #=======================================================================
        # self.GageOilTemp.SetMiddleText("OIL C")
        # self.GageOilTemp.SetMiddleTextColour(wx.WHITE)
        # self.GageOilTemp.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        #=======================================================================
         
        self.GageOilTemp.SetSpeedValue(40)

        # End Of SpeedMeter Controls Construction. Add Some Functionality
        self.isalive = 0



        # These Are Cosmetics For SpeedMeter Controls
        bsizerkmh = wx.BoxSizer(wx.VERTICAL)
        hsizerkmh = wx.BoxSizer(wx.HORIZONTAL)   
        bsizerkmh.Add(self.GageKmh, 1, wx.EXPAND) 
        stattextkmh = wx.StaticText(panelkmh, -1, "Km/h", style=wx.ALIGN_CENTER)     
        stattextkmh.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
        hsizerkmh.Add(stattextkmh, 1, wx.EXPAND)
        bsizerkmh.Add(hsizerkmh, 0, wx.EXPAND)
        panelkmh.SetSizer(bsizerkmh)
       
       
        bsizerrpm = wx.BoxSizer(wx.VERTICAL)
        hsizerrpm = wx.BoxSizer(wx.HORIZONTAL)
        bsizerrpm.Add(self.GageRPM, 1, wx.EXPAND) 
        stattextrpm = wx.StaticText(panelrpm, -1, "RPM x 100", style=wx.ALIGN_CENTER)
        stattextrpm.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
        hsizerrpm.Add(stattextrpm, 1, wx.EXPAND)       
        bsizerrpm.Add(hsizerrpm, 0, wx.EXPAND)       
        panelrpm.SetSizer(bsizerrpm)
        
        bsizerairtemp = wx.BoxSizer(wx.VERTICAL)        
        hsizerairtemp = wx.BoxSizer(wx.HORIZONTAL)                
        bsizerairtemp.Add(self.GageAirTemp, 1, wx.EXPAND)
        stattextairtemp = wx.StaticText(panelairtemp, -1, "Air Temp", style=wx.ALIGN_CENTER)
        stattextairtemp.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
        hsizerairtemp.Add(stattextairtemp, 1, wx.EXPAND)
        bsizerairtemp.Add(hsizerairtemp, 0, wx.EXPAND)
        panelairtemp.SetSizer(bsizerairtemp)
        
        bsizerblocktemp = wx.BoxSizer(wx.VERTICAL)
        hsizerblocktemp = wx.BoxSizer(wx.HORIZONTAL)                      
        bsizerblocktemp.Add(self.GageBlockTemp, 1, wx.EXPAND)
        stattextblocktemp = wx.StaticText(panelblocktemp, -1, "Block Temp", style=wx.ALIGN_CENTER)
        stattextblocktemp.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
        hsizerblocktemp.Add(stattextblocktemp, 1, wx.EXPAND)
        bsizerblocktemp.Add(hsizerblocktemp, 0, wx.EXPAND)
        panelblocktemp.SetSizer(bsizerblocktemp)
        
        bsizerintaketemp = wx.BoxSizer(wx.VERTICAL)
        hsizerintaketemp = wx.BoxSizer(wx.HORIZONTAL)                    
        bsizerintaketemp.Add(self.GageIntakeTemp, 1, wx.EXPAND)
        stattextintaketemp= wx.StaticText(panelintaketemp, -1, "Intake Temp", style=wx.ALIGN_CENTER)
        stattextintaketemp.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
        hsizerintaketemp.Add(stattextintaketemp, 1, wx.EXPAND)
        bsizerintaketemp.Add(hsizerintaketemp, 0, wx.EXPAND)
        panelintaketemp.SetSizer(bsizerintaketemp)
        
        bsizeroiltemp = wx.BoxSizer(wx.VERTICAL)
        hsizeroiltemp = wx.BoxSizer(wx.HORIZONTAL)
        bsizeroiltemp.Add(self.GageOilTemp, 1, wx.EXPAND)
        stattextoiltemp = wx.StaticText(paneloiltemp, -1, "Oil Temp", style=wx.ALIGN_CENTER)
        stattextoiltemp.SetFont(wx.Font( 5, 74, 90, 90, False, "Calibri" )) 
        hsizeroiltemp.Add(stattextoiltemp, 1, wx.EXPAND)
        bsizeroiltemp.Add(hsizeroiltemp, 0, wx.EXPAND)
        paneloiltemp.SetSizer(bsizeroiltemp)
        
        
        #=======================================================================
        # bsizerkmh.Layout()
        # bsizerrpm.Layout()
        # bsizerairtemp.Layout()
        # bsizerblocktemp.Layout()
        # bsizerintaketemp.Layout()
        # bsizeroiltemp.Layout()
        #=======================================================================
        
        #=======================================================================
        # displayKmh = self.cfg.ReadBool('           Vehicle Speed')
        # displayRPM = self.cfg.ReadBool('              Engine RPM')
        # displayCoolantTemp = self.cfg.ReadBool('     Coolant Temperature')
        # displayIntake = self.cfg.ReadBool('         Intake Air Temp')
        # displayLoad = self.cfg.ReadBool('   Calculated Load Value')
        # displayMAF = self.cfg.ReadBool('     Air Flow Rate (MAF)')
        #=======================================================================
        if displayKmh: sizerGraphical.Add(panelkmh,  1, wx.EXPAND)
        if displayRPM: sizerGraphical.Add(panelrpm,  1, wx.EXPAND)
        if displayLoad: sizerGraphical.Add(panelairtemp,  1, wx.EXPAND) #invent
        if displayCoolant: sizerGraphical.Add(panelblocktemp, 1, wx.EXPAND) #invent
        if displayIntake: sizerGraphical.Add(panelintaketemp, 1, wx.EXPAND)  
        if displayMAF: sizerGraphical.Add(paneloiltemp,  1, wx.EXPAND) #invent

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

        
        #self.SetSizer( bSizer2 )
        #=======================================================================
        # self.Layout()
        # 
        # self.Centre( wx.BOTH )
        #=======================================================================
    def ShowSensors(self):
        
        sensors = self.getSensorsToDisplay(self.istart)

        # Destroy previous widgets
        for b in self.boxes: b.Destroy()
        for t in self.texts: t.Destroy()
        self.boxes = []
        self.texts = []

        # Main sizer
        boxSizerMain = wx.BoxSizer(wx.VERTICAL)

        # Grid sizer
        nrows, ncols = 1, 1
        vgap, hgap = 50, 50
        gridSizer = wx.GridSizer(nrows, ncols, vgap, hgap)

        # Create a box for each sensor
#===============================================================================
#         for index, sensor in sensors:
#             
#             (name, value, unit) = self.port.sensor(index)
# 
#             box = OBDStaticBox(self, wx.ID_ANY)
#             self.boxes.append(box)
#             boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
# 
#             # Text for sensor value 
#             if type(value)==float:  
#                 value = str("%.2f"%round(value, 3))                    
#             t1 = wx.StaticText(parent=self, label=str(value), style=wx.ALIGN_CENTER)
#             t1.SetForegroundColour('WHITE')
#             font1 = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL, faceName="Monaco")
#             t1.SetFont(font1)
#             boxSizer.Add(t1, 0, wx.ALIGN_CENTER | wx.ALL, 70)
#             boxSizer.AddStretchSpacer()
#             self.texts.append(t1)
# 
#             # Text for sensor name
#             t2 = wx.StaticText(parent=self, label=name, style=wx.ALIGN_CENTER)
#             t2.SetForegroundColour('WHITE')
#             font2 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD, faceName="Monaco")
#             t2.SetFont(font2)
#             boxSizer.Add(t2, 0, wx.ALIGN_CENTER | wx.ALL, 45)
#             self.texts.append(t2)
#             gridSizer.Add(boxSizer, 1, wx.EXPAND | wx.ALL)
#===============================================================================

        # Add invisible boxes if necessary
        #=======================================================================
        # nsensors = len(sensors)
        # for i in range(1-nsensors):
        #     box = OBDStaticBox(self)
        #     boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        #     self.boxes.append(box)
        #     box.Show(False)
        #     gridSizer.Add(boxSizer, 1, wx.EXPAND | wx.ALL)
        #=======================================================================
           
        # Layout
        boxSizerMain.Add(gridSizer, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(boxSizerMain)
        self.Refresh()
        self.Layout() 
    
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
    

#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import os



class OBD_Capture():
    def __init__(self):
        self.supportedSensorList = []
        self.port = None
        localtime = time.localtime(time.time())

    def connect(self):
        portnames = self.scanSerial()
        print portnames
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        
    def getSupportedSensorList(self):
        print "getsuppsenslist"
        print self.supportedSensorList 
        return self.supportedSensorList 
    
    def getUnSupportedSensorList(self):
        return self.unsupportedSensorList
    
    def getrecordfile(self):
        return self.record_file

    
    def record(self):
        print "recording"
        line=""
        #supported_sensor_list= self.get_supported_sensor_list()
        self.supp = self.port.sensor(0)[1]
        self.supportedSensorList = []
        self.unsupportedSensorList = []
        #filerecord= self.getrecordfile()
        
        
        for i in range(0, len(self.supp)):
            if self.supp[i] == "1":
                # store index of sensor and sensor object
                self.supportedSensorList.append([i+1, obd_sensors.SENSORS[i+1]])
            else:
                self.unsupportedSensorList.append([i+1, obd_sensors.SENSORS[i+1]])
        
        for supportedSensor in self.supportedSensorList:
            line += "suported sensors: " + str(supportedSensor[0]) + " " + str(supportedSensor[1].shortname) + "\n"
        print line
        time.sleep(3)
               
        if(self.port is None):
            return None
              
         
        line = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')+ ";"  +"index" + ";"+ "name"+ "\n"
      
        for supportedSensor in self.supportedSensorList:
            sensorIndex = supportedSensor[0]
            (name, value, unit) = self.port.sensor(sensorIndex)
            line += name + ";" + str(value) + ";" + str(unit) + "\n"
        #self.write_record(filerecord, line)
        return line

            
    
    def write_record(self,file_record,line):   
        f = open(file_record, 'w')
        f.write(line) #Give your csv text here.
        f.close()
    
    def capture_dtc(self):
        self.DTCCodes=[]
        self.DTCCodes = self.port.get_dtc() 
        print self.DTCCodes
        return self.DTCCodes
    
    def capture_dtc_f(self):
        self.DTCFCodes=[]
        self.DTCFCodes = self.port.get_dtc_f() 
        print self.DTCFCodes
        return self.DTCFCodes
        
    def clear_dtc(self):
        self.result=self.port.clear_dtc()
        print self.result
        return self.result
       
    def setPort(self, port):
        self.port = port 
        
    def scanSerial(self):
        available = []
        for i in range(10):
          try:
            s = serial.Serial("/dev/rfcomm"+str(i))
            available.append( (str(s.port)))
            s.close()   # explicit close 'cause of delayed GC in java
          except serial.SerialException:
            pass
        return available
    
if __name__ == "__main__":

    o = OBD_Capture()
    o.connect()
    time.sleep(3)
    if not o.is_connected():
        print "Not connected"
    else:
        o.record()

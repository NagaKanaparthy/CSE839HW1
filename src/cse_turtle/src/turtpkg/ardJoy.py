#!/usr/bin/env python
from sensor_msgs.msg import Joy 
import rospy
import serial, struct
import time

class ArdJoy:
   
    def __init__(self, portName):
        try:
            self.port = port = serial.Serial(port=portName, baudrate=9600)
            self.seq = 0
            self.stamp = rospy.Time.now()
            self.frameId = 1
            self.buttonPacketDict = { 0 : 1, 1 : 13, 2 : 14, 3 : 15, 4 : 12}
            self.joyPacketDict = {5 : 0, 7 : 1}
            self.buttonArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            self.joyArray = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            self.deadzone = 0.05
        except:
            print "Joy Not Connected"
    
    def getMessage(self):
        firstVal = self.port.read()
        value = struct.unpack('B', firstVal)[0]
        if(value == 6):
            msg = self.port.read(5)
            packet = ArdJoy.readPacket(msg)
            if(packet[0]+packet[1] == packet[2]):
                messageToPublish = self.convertPacket(packet)
                self.buttonArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                return messageToPublish
        return None
    
    def convertPacket(self, packet):
        if(packet[0] in [0,1,2,3,4]):
            self.buttonArray[self.buttonPacketDict[packet[0]]] = packet[1]
        if(packet[0] in [5,7]):
            val = float(packet[1])
            print  "Joy #:"+str(packet[0])+" -  Val : "+str(val)
            if(val >= 512.00):
                val = (val - 512.00)/512.00
            else:
                val = (val - 1023.00)/512.00
            if(val > self.deadzone and val < -self.deadzone):
                self.joyArray[self.joyPacketDict[packet[0]]] = val
        joyNode = Joy()
        joyNode.buttons = self.buttonArray
        joyNode.axes = self.joyArray
        joyNode.header.stamp = rospy.Time.now()
        joyNode.header.seq = self.seq
        joyNode.header.frame_id = 1
        self.seq += 1
        return joyNode

    @classmethod
    def readPacket(cls, msg):
        header = struct.unpack('B', msg[0])[0]
        funcVal = struct.unpack('>H', msg[1:3])[0]
        checkSum = struct.unpack('>H', msg[3:])[0]
        return [header, funcVal, checkSum]
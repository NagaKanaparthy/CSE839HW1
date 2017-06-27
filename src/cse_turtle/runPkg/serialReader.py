#! /usr/bin/env python

import rospy
import serial, struct
import time
from std_msgs.msg import String

def readPacket(msg):
      header = struct.unpack('B', msg[0])[0]
      funcVal = struct.unpack('>H', msg[1:3])[0]
      checkSum = struct.unpack('>H', msg[3:])[0]
      return [header, funcVal, checkSum]

def talker():
    pub = rospy.Publisher('ps3joy', String, queue_size=10)
    rospy.init_node('rx', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        port = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
        firstVal = port.read()
        value = struct.unpack('B', firstVal)[0]
        if(value == 6):
              msg = port.read(5)
              packet = readPacket(msg)
              print('header: '+str(packet[0])+'\nfuncVal: '+str(packet[1])+'\nCheckSum: '+str(packet[2]))
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
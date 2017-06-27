#! /usr/bin/env python

from sensor_msgs.msg import Joy 
from turtpkg.ardJoy import ArdJoy
import rospy
import serial, struct
import time

def pubber():
    pub = rospy.Publisher('joy', Joy, queue_size=10)
    rospy.init_node('joyReader', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    joyPad = ArdJoy('/dev/ttyACM0')
    while not rospy.is_shutdown():
        data = joyPad.getMessage()
        if(data is not None):
            rospy.loginfo(data)
            pub.publish(data)
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        pubber()
    except rospy.ROSInterruptException:
        pass
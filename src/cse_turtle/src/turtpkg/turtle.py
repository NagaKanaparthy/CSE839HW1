#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import radians
from std_msgs.msg import String
from std_srvs.srv import Empty
from turtlesim.srv import Kill
from turtlesim.srv import Spawn

class Turtle:
    def __init__(self, name):
        self.name = name

    def prepareForMovement(self):
        self.mover = rospy.Publisher('/'+self.name+'/cmd_vel', Twist, queue_size=10)
    
    def kill(self):
        rospy.wait_for_service('kill')
        turtleKiller = rospy.ServiceProxy('kill',Kill)
        try:
            turtleKiller(self.name)
        except rospy.ServiceException, e:
            print "Kill service call failed: %s" % e

    def spawn(self, xPos, yPos, angle):
        rospy.wait_for_service('spawn')
        spawner = rospy.ServiceProxy('spawn', Spawn)
        try:
            spawner(xPos,yPos,radians(angle),self.name)
        except rospy.ServiceException, e:
            print "Kill service call failed: %s" % e

    def rotate(self, angle):
        command = Twist()
        radVal = 2*angle*3.141/360
        angleSpeed = radVal/3
        command.angular.z = angleSpeed
        t0 = rospy.Time.now().to_sec()
        t1 = rospy.Time.now().to_sec()
        currentAngle = 0
        while(t1 - t0 < 3):
            self.mover.publish(command)
            t1 = rospy.Time.now().to_sec()
        command.angular.z = 0
        self.mover.publish(command)

    def move(self, distance):
        command = Twist()
        speed = distance
        command.linear.x = speed
        t0 = rospy.Time.now().to_sec()
        t1 = rospy.Time.now().to_sec()
        currentDis = 0
        if(distance > 0):
            while(currentDis < distance):
                self.mover.publish(command)
                t1 = rospy.Time.now().to_sec()
                currentDis = (t1-t0)*speed
        else:
            while(currentDis > distance):
                self.mover.publish(command)
                t1 = rospy.Time.now().to_sec()
                currentDis = (t1-t0)*speed
        command.linear.x = 0
        self.mover.publish(command)
    
    @classmethod
    def clear(cls):
        rospy.wait_for_service('clear')
        clearer = rospy.ServiceProxy('clear',Empty)
        try:
            clearer()
        except rospy.ServiceException, e:
            print "Kill service call failed: %s" % e
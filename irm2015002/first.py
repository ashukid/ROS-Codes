#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist,Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import tf
import math
import random
from helper import *


goalid=1
goal=getGoal(goalid)

fx=0
fy=0

posx=0
posy=0
theta=0
flag=1

def twistMsg():

    global posx,posy,theta,goal,goalid,flag

    msg=Twist()

    adiff=math.atan2(fy,fx) - theta
    adiff=math.atan2(math.sin(adiff),math.cos(adiff))


    xdiff=goal[0]-posx
    ydiff=goal[1]-posy

    ddiff=math.sqrt(math.pow(ydiff,2)+math.pow(xdiff,2))

    if(ddiff<1.5):
        # msg.linear.x=0
        # msg.angular.z=0
        # flag=0
        # print(posx,posy)

        rn=random.randint(1,10)
        if(rn<=6):
            goalid = 4-goalid
        if(rn<=8 and rn>6):
            goalid = 2
        else:
            goalid = 4
        

        goal=getGoal(goalid)

    if(flag):
        if(adiff>0.1):
            msg.angular.z = adiff
        if(adiff<-0.1):
            msg.angular.z = adiff

        msg.linear.x = 1
    return msg 



def posCallback(data):

    global goal,theta,posx,posy
    trans=data[0]
    rot=data[1]
    quaternion = (rot[0],rot[1],rot[2],rot[3])
    euler = euler_from_quaternion(quaternion)

    theta=euler[2]
    posx=trans[0]
    posy=trans[1]

    # print(posx,posy)


def talker():

    rospy.init_node('talker1', anonymous=True)
    pub = rospy.Publisher('/r1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    listener=tf.TransformListener()
    listener.waitForTransform('/r1_odom','/r1_base_link',rospy.Time(0),rospy.Duration(5))
    listener.waitForTransform('/r1_odom','/r2_base_link',rospy.Time(0),rospy.Duration(5))
    listener.waitForTransform('/r1_odom','/r3_base_link',rospy.Time(0),rospy.Duration(5))
    listener.waitForTransform('/r1_odom','/r4_base_link',rospy.Time(0),rospy.Duration(5))

    while not rospy.is_shutdown():
       
        (trans1,rot1)=listener.lookupTransform('/r1_odom','/r1_base_link',rospy.Time(0))
        (trans2,rot2)=listener.lookupTransform('/r1_odom','/r2_base_link',rospy.Time(0))
        (trans3,rot3)=listener.lookupTransform('/r1_odom','/r3_base_link',rospy.Time(0))
        (trans4,rot4)=listener.lookupTransform('/r1_odom','/r4_base_link',rospy.Time(0)) 


        global fx,fy,goal

        mine=[trans1,rot1]
        posCallback(mine)

        others=[trans2,trans3,trans4]
        fx,fy=calForces(mine[0],others,goal)

        msg=twistMsg()
        pub.publish(msg)
        rate.sleep()

    rospy.spin()    


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
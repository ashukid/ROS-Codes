#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist,Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math


goalx=0
goaly=0
goaltheta=0
posx=0
posy=0
theta=0

def twistMsg():
    global goalx,goaly,goaltheta,posx,posy,theta

    msg=Twist()

    ydiff=goaly-posy
    xdiff=goalx-posx

    adiff=math.atan2(ydiff,xdiff)- theta
    adiff=math.atan2(math.sin(adiff),math.cos(adiff))
    ddiff=math.sqrt(math.pow(ydiff,2)+math.pow(xdiff,2))

    msg.angular.z = adiff
    msg.linear.x = min(ddiff,1)

        
    return msg


def goalCallback(data):

    global goalx,goaly,goaltheta

    quaternion = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w)
    euler = euler_from_quaternion(quaternion)

    goalx=data.pose.pose.position.x
    goaly=data.pose.pose.position.y + 1
    goaltheta=euler[2]


def posCallback(data):

    global theta,posx,posy

    quaternion = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w)
    euler = euler_from_quaternion(quaternion)

    theta=euler[2]
    posx=data.pose.pose.position.x
    posy=data.pose.pose.position.y

def talker():

    rospy.Subscriber('/r2/pose',Odometry,goalCallback)
    rospy.Subscriber('/r3/pose',Odometry,posCallback)
    pub = rospy.Publisher('/r3/cmd_vel', Twist, queue_size=10)
    
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz


    while not rospy.is_shutdown():
       
        msg=twistMsg()
        # rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
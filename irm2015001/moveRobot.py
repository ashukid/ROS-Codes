#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import tf

def moveRobot():


    pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) 
    listener=tf.TransformListener()


    while not rospy.is_shutdown():
        vel = Twist()
        vel.linear.x=1
        vel.linear.y=0
        vel.linear.z=0
        vel.angular.x=0
        vel.angular.y=0
        vel.angular.z=1


        (trans,rot)=listener.lookupTransform('RosAria_odom','world',rospy.Time(0))
        print(str(trans)+' '+str(rot))

        rospy.loginfo(vel)
        pub.publish(vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        moveRobot()
    except rospy.ROSInterruptException:
        pass
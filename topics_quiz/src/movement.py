#! /usr/bin/env python
import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(msg):
	print(msg.ranges[0])
	if msg.ranges[0] < 1:
		#Stop turn right
		turn.linear.x = 0
		turn.angular.z = 0
		pub.publish(turn)
		time.sleep(2)
		turn.angular.z = 0.5
		pub.publish(turn)
		time.sleep(0.5)
		turn.linear.x = 0
		turn.angular.z = 0
		pub.publish(turn)
	#Mers inapoi
	turn.linear.x = -0.5
	pub.publish(turn)

rospy.init_node("topic_publisher")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
sub = rospy.Subscriber("/scan",LaserScan, callback)

rate = rospy.Rate(2)
turn = Twist()
rospy.spin()


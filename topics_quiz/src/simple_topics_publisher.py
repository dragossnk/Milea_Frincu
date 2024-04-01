! /usr/bin/env python

import rospy
from std_msgs.msg import Int32

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/counter', Int32, queue_size=1)
rate = rospy.Rate(2)
count = Int32()
count.data = 0
while not rospy.is_shutdown(): # Create a loop that will go until someone stops the program execution
	pub.publish(count) # Publish the message within the 'count' variable
	count.data += 1 # Increment 'count' variable
	rate.sleep()

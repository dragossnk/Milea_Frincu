#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import Twist, PoseStamped
from tf.transformations import euler_from_quaternion
from actions_quiz.msg import OrientationAction, OrientationGoal, OrientationResult, OrientationFeedback

def feedback_callback(feedback):
    pass

def pose_callback(pose):
    orientation = pose.pose.orientation
    orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
    roll, pitch, yaw = euler_from_quaternion(orientation_list)

def move_in_circle():
    rospy.init_node('circle_movement_client')
    rospy.Subscriber('/odom', PoseStamped, pose_callback)
    client = actionlib.SimpleActionClient('my_action_server', OrientationAction)
    client.wait_for_server()
    
    goal = OrientationGoal(duration=10)
    client.send_goal(goal, feedback_cb=feedback_callback)
    
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown() and client.get_state() < 2:
        twist = Twist()
        twist.linear.x = 0.2
        twist.angular.z = 0.5
        cmd_vel_pub.publish(twist)
        rate.sleep()
    
    cmd_vel_pub.publish(Twist())

if __name__ == '__main__':
    try:
        move_in_circle()
    except rospy.ROSInterruptException:
        pass

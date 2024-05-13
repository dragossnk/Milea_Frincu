#!/usr/bin/env python

import rospy
import actionlib

from actions_quiz.msg import OrientationAction, OrientationFeedback, OrientationResult
from geometry_msgs.msg import PoseStamped

class OrientationServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer("my_action_server", OrientationAction, self.execute, False)
        self.server.start()
        self.pose_subscriber = rospy.Subscriber('/pose_topic', PoseStamped, self.pose_callback)
        self.current_orientation_w = 0.0
    
    def pose_callback(self, msg):
        self.current_orientation_w = msg.pose.orientation.w
    
    def execute(self, goal):
        rate = rospy.Rate(1) 
        orientations = []
        start_time = rospy.Time.now()
        
        while (rospy.Time.now() - start_time).to_sec() < goal.duration:
            if self.server.is_preempt_requested():
                self.server.set_preempted()
                break
            feedback = OrientationFeedback()
            feedback.distance = self.current_orientation_w 
            self.server.publish_feedback(feedback)
            orientations.append(self.current_orientation_w)
            rate.sleep()

        result = OrientationResult()
        result.success = "Success"  # Set success message
        self.server.set_succeeded(result)

if __name__ == '__main__':
    rospy.init_node('orientation_server_node')
    server = OrientationServer()
    rospy.spin()

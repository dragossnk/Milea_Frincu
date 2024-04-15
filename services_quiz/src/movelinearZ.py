#!/usr/bin/env python

import rospy
from datetime import datetime
from services_quiz.srv import ServMess, ServMessResponse
from geometry_msgs.msg import Twist

def my_callback(request):
    print("my_callback has been called")
    start_time = datetime.now()
    turn = Twist()
    
    if request.duration <= 0:
        rospy.logwarn("Duration should be a positive value")
        response = ServMessResponse()
        response.success = False
        return response

    if request.direction == 'up':
        turn.linear.z = 0.5  # Move up
    elif request.direction == 'down':
        turn.linear.z = -0.5  # Move down
    else:
        rospy.logwarn("Invalid direction. Please specify 'up' or 'down'.")
        response = ServMessResponse()
        response.success = False
        return response

    while (datetime.now() - start_time).total_seconds() < request.duration:
        pub.publish(turn)
        rospy.sleep(0.1)  # Adjust as needed

    turn.linear.z = 0.0  # Stop linear motion
    pub.publish(turn)
    
    response = ServMessResponse()
    response.success = True
    return response

if __name__ == "__main__":
    rospy.init_node('service_server')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    my_service = rospy.Service('/my_service', ServMess, my_callback)
    rospy.spin()

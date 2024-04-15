#!/usr/bin/env python

import rospy
from datetime import datetime
from services_quiz.srv import ServMess, ServMessResponse
from geometry_msgs.msg import Twist

def my_callback(request):
    print("my_callback has been called")
    move = Twist()
    i = 0
    duration = request.duration 
    start_time = rospy.get_time()
    
    while start_time + duration > rospy.get_time() :
        if request.direction == 'up':
            move.linear.z = 2
            pub.publish(move)
        elif request.direction == 'down':
            move.linear.z = -2
            pub.publish(move)
        
        i += 1
        rate.sleep()
    
    move.linear.z = 0
    move.linear.x = 0  # Assuming you want to stop other linear movement axes
    move.linear.y = 0  # Assuming you want to stop other linear movement axes
    pub.publish(move)
    
    response = ServMessResponse()
    response.success = True
    return response

if __name__ == "__main__":
    rospy.init_node('service_server')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    my_service = rospy.Service('/my_service', ServMess, my_callback)
    rospy.spin()

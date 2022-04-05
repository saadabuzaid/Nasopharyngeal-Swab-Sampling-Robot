#!/usr/bin/python
#
# Send joint values to UR5 using messages
#

from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory

from trajectory_msgs.msg import JointTrajectoryPoint
import rospy
import cv2
import sys
import numpy as np
import message_filters
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


waypoints = [[0.0, -1.5708, 1.5708, 0.6, 0, -0.33], [0,0,0,0,0,0]]
faceDetected = 0
class face_detector:

    def __init__(self):
        self.bridge = CvBridge()
    
        self.image_sub = rospy.Subscriber("/kinect/color/image_raw", Image, self.callback)
    
        self.pub = rospy.Publisher('/unibas_face_detector/faces', Image, queue_size=1)	

    def callback(self, rgb_data):
    
        try:
            img = self.bridge.imgmsg_to_cv2(rgb_data, "bgr8")
            face_cascade = cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')
            #face_cascade.load('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print"Number of faces detected",len(faces)
            if(len(faces) > 0):
                faceDetected = 1
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
            
        except CvBridgeError as e:
            print(e)
        
        cv2.imshow("faces", img)
        cv2.waitKey(30)

    #convert opencv format back to ros format and publish result
        try:
            faces_message = self.bridge.cv2_to_imgmsg(img, "bgr8")
            self.pub.publish(faces_message)
        except CvBridgeError as e:
            print(e)
    


"""
def faceDetected():
    image = cv2.imread("/home/saadabuzaid/CE301_saad_saad_a_s_a/catkin_ws/src/ce301_pkg/scripts/haarcascadeXMLFiles/testImage.png")
    cv2.imshow("Check",image)
    cv2.waitKey()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascade/haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image_gray,1.1,5)
    for x, y, width, height in faces:
        cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
    if len(faces) == 1:
        return true
    else:
        return false

"""
def main():

    fd = face_detector()

    rospy.init_node('send_joints')
    pub = rospy.Publisher('/arm_controller/command',
                          JointTrajectory,
                          queue_size=10)

    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR5
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(1)
    elbow_joint = 1.5708
    wrist_1_joint = 0.6
    pts = JointTrajectoryPoint()
    traj.header.stamp = rospy.Time.now()

    while not rospy.is_shutdown():
        elbow_joint -= 0.1
        wrist_1_joint -= 0.1
        print "elbow_joint is: %d wrist_1_joint is: %d",(elbow_joint,wrist_1_joint)
        pts.positions = [0.0, -1.5708, 0.2708 , wrist_1_joint, 0, -0.33]
        pts.time_from_start = rospy.Duration(1.0)

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        pub.publish(traj)
        rate.sleep()
        if(faceDetected):
            break
            print("Face Detected")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")

#!/usr/bin/env python
from __future__ import print_function

from std_msgs.msg import Header
import roslib
roslib.load_manifest('unibas_face_distance_calculator')
import sys
import rospy
import cv2
import numpy as np
import message_filters
from std_msgs.msg import String
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import math
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

class face_detector:

    def test(self,sa,saa,saad):
        print("testttt")
        cv_rgb = self.bridge.imgmsg_to_cv2(sa, "bgr8")  
        print("Bridged")
        
        face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
        gray = cv2.cvtColor(cv_rgb, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces)>0:
            self.stop_flag = True
            #else:
                #self.move()
        rgb_height, rgb_width, rgb_channels = cv_rgb.shape
        for (x,y,w,h) in faces:
            cv2.rectangle(cv_rgb,(x,y),(x+w,y+h),(255,0,0),2)
            #cv2.rectangle(cv_depth,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(cv_rgb,(x+30,y+30),(x+w-30,y+h-30),(0,0,255),2)
            #cv2.rectangle(cv_depth,(x+30,y+30),(x+w-30,y+h-30),(0,0,255),2)
            #roi_depth = depth_image[y+30:y+h-30, x+30:x+w-30]    
        cv2.imshow("TEST",cv_rgb)
        cv2.waitKey(500)
        

    def __init__(self):     
        
       # rospy.init_node('CE301')
        self.bridge = CvBridge()
    
        self.camera_info_sub = message_filters.Subscriber('/kinect/color/camera_info', CameraInfo)
           	
        self.image_sub = message_filters.Subscriber("/kinect/color/image_raw",Image)
        self.depth_sub = message_filters.Subscriber("/kinect/depth/image_raw",Image)
        
        self.ts = message_filters.ApproximateTimeSynchronizer([self.image_sub, self.depth_sub, self.camera_info_sub],queue_size = 10, slop = 0.2)
        self.ts.registerCallback(self.update_msgs)
        self.pub = rospy.Publisher('/unibas_face_distance_calculator/faces', Image, queue_size=1)
        self.stop_flag = False	
    
    
    def update_msgs(self,rgb_data,depth_data,camera_info):
        self.camera_info = camera_info
        self.rgb_data = rgb_data
        self.depth_data = depth_data
    
    
    
        
    def callback(self, rgb_data, depth_data, camera_info):
        print("CALLBACK")
        try:
            camera_info_K = np.array(camera_info.K)
          
          # Intrinsic camera matrix for the raw (distorted) images.
          #     [fx  0 cx]
          # K = [ 0 fy cy]
          #     [ 0  0  1]
        
            m_fx = camera_info.K[0];
            m_fy = camera_info.K[4];
            m_cx = camera_info.K[2];
            m_cy = camera_info.K[5];
            inv_fx = 1. / m_fx;
            inv_fy = 1. / m_fy;
        
            print("1")
            cv_rgb = self.bridge.imgmsg_to_cv2(rgb_data, "bgr8")
            depth_image = self.bridge.imgmsg_to_cv2(depth_data, "32FC1")
            depth_array = np.array(depth_image, dtype=np.float32)
            cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
            depth_8 = (depth_array * 255).round().astype(np.uint8)
            cv_depth = np.zeros_like(cv_rgb)
            cv_depth[:,:,0] = depth_8
            cv_depth[:,:,1] = depth_8
            cv_depth[:,:,2] = depth_8
            print("2")
            face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
            gray = cv2.cvtColor(cv_rgb, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces)>0:
                self.stop_flag = True
            
            rgb_height, rgb_width, rgb_channels = cv_rgb.shape
            for (x,y,w,h) in faces:
                cv2.rectangle(cv_rgb,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.rectangle(cv_depth,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.rectangle(cv_rgb,(x+30,y+30),(x+w-30,y+h-30),(0,0,255),2)
                cv2.rectangle(cv_depth,(x+30,y+30),(x+w-30,y+h-30),(0,0,255),2)
                roi_depth = depth_image[y+30:y+h-30, x+30:x+w-30]
            
                n = 0
                sum = 0
                for i in range(0,roi_depth.shape[0]):
                    for j in range(0,roi_depth.shape[1]):
                        value = roi_depth.item(i, j)
                        if value > 0.:
                            n = n + 1
                            sum = sum + value
            
                mean_z = sum / n
            
                point_z = mean_z ; # distance in meters
                point_x = ((x + w/2) - m_cx) * point_z * inv_fx;
                point_y = ((y + h/2) - m_cy) * point_z * inv_fy;
            
                x_str = "X: " + str(format(point_x, '.2f'))
                y_str = "Y: " + str(format(point_y, '.2f'))
                z_str = "Z: " + str(format(point_z, '.2f'))
                    
                cv2.putText(cv_rgb, x_str, (x+w, y), cv2.FONT_HERSHEY_SIMPLEX,  
                       0.7, (0,0,255), 1, cv2.LINE_AA) 
                cv2.putText(cv_rgb, y_str, (x+w, y+20), cv2.FONT_HERSHEY_SIMPLEX,  
                       0.7, (0,0,255), 1, cv2.LINE_AA)
                cv2.putText(cv_rgb, z_str, (x+w, y+40), cv2.FONT_HERSHEY_SIMPLEX,  
                       0.7, (0,0,255), 1, cv2.LINE_AA)
                       
                dist = math.sqrt(point_x * point_x + point_y * point_y + point_z * point_z)
            
                dist_str = "dist:" + str(format(dist, '.2f')) + "m"
            
                cv2.putText(cv_rgb, dist_str, (x+w, y+60), cv2.FONT_HERSHEY_SIMPLEX,  
                       0.7, (0,255,0), 1, cv2.LINE_AA)
            print("3")
            cv2.imshow("IMAGETRIAL",cv_rgb)
            cv2.waitKey(500)
            
        except CvBridgeError as e:
            print(e)
      
        rgbd = np.concatenate((cv_rgb, cv_depth), axis=1)

    #convert opencv format back to ros format and publish result
        
    
        print("4")
    def nostrilsDetection(self, gray, img):
        print("Entered nostrilDetection function")
        predictor = dlib.shape_predictor('/home/saadabuzaid/CE301_saad_saad_a_s_a/catkin_ws/src/ce301_pkg/scripts/shape_predictor_68_face_landmarks.dat')
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        print(len(faces))
        for face in faces:
            landmark = predictor(image=gray,box=face)
            x1 = landmark.part(32).x
            y1 = landmark.part(32).y
            x2 = landmark.part(34).x
            y2 = landmark.part(34).y
            cv2.circle(img=img,center=(x1,y1),radius=5,color=(0,255,0),thickness=-1)
            cv2.circle(img=img,center=(x2,y2),radius=5,color=(0,255,0),thickness=-1)



    def move(self):

    
        
        rospy.init_node('send_joints',anonymous=False)
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

        rate = rospy.Rate(0.6)
        elbow_joint = 1.5708
        wrist_1_joint = 0.6
        pts = JointTrajectoryPoint()
        pts.positions = [0.0, -1.5708, 0.2708 ,0.6,0, -0.33]
       

        while not rospy.is_shutdown() and not self.stop_flag:
        
            elbow_joint -= 0.1
            wrist_1_joint -= 0.1
            print("elbow_joint is: %d wrist_1_joint is: %d",(elbow_joint,wrist_1_joint))
            pts.positions = [0.0, -1.5708, 0.2708 , wrist_1_joint, 0, -0.33]
            pts.time_from_start = rospy.Duration(1.0)

            # Set the points to the trajectory
            traj.points = []
            traj.points.append(pts)
            # Publish the message
            pub.publish(traj)
            rate.sleep()
            self.callback(self.rgb_data,self.depth_data,self.camera_info)    
        print("OUT OF LOOP")
        #self.nostrilsDetection
        #self.callback

if __name__ == '__main__':
    try:
        fd = face_detector()
        fd.move()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
    


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


class swab_sampling_robot:


    def __init__(self):
        self.bridge = CvBridge()
        
        
        
    def face_detector(self,rgb):
        print"INSIDEface_detector"
    
        try:
            img = self.bridge.imgmsg_to_cv2(rgb_data, "bgr8")
            face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
            #face_cascade.load('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print"Number of faces detected",len(faces)
            if(len(faces) > 0):
                self.stop_flag = True
                self.nostrilsDetection(gray,img)
            else: 
                self.move
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
            
            #detector = dlib.get_frontal_face_detector()

            
        except CvBridgeError as e:
            print(e)
        
        cv2.imshow("faces", img)
        cv2.waitKey(30)
        
        
    def nostrilsDetection(self, gray, img):
        print "Entered nostrilDetection function"
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
            
    def distanceCalc():
        depth_image = self.bridge.imgmsg_to_cv2(depth_data, "32FC1")
        depth_array = np.array(depth_image, dtype=np.float32)
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
        depth_8 = (depth_array * 255).round().astype(np.uint8)
        cv_depth = np.zeros_like(cv_rgb)
        cv_depth[:,:,0] = depth_8
        cv_depth[:,:,1] = depth_8
        cv_depth[:,:,2] = depth_8
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
        
    
        


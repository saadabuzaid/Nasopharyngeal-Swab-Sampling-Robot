#!/usr/bin/python
#
# Send joint values to UR5 using messages
#

from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory

from trajectory_msgs.msg import JointTrajectoryPoint
import rospy

waypoints = [[0.0, -1.5708, 1.5708, 0.6, 0, -0.33], [0,0,0,0,0,0]]
"""
def faceDetected():
	#get image from camera on robot
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	face_cascade = cv2.CascadeClassifier("haarcascade_fontalface_default.xml")
	# detect all the faces in the image
	faces = face_cascade.detectMultiScale(image_gray,1.1,4)
	# print the number of faces detected
	print("{len(faces)} faces detected in the image.")
	for x, y, width, height in faces:
    	cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
	cv2.imwrite("face_detected.jpg", image)
	if(len(faces) == 0)
		return false
	else
		return true
"""
def main():

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
        pts.positions = [0.0, -1.5708, elbow_joint, wrist_1_joint, 0, -0.33]
        pts.time_from_start = rospy.Duration(1.0)

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        pub.publish(traj)
        rate.sleep()
        #if(faceDetected)
			#break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")

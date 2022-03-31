#!/usr/bin/python


import cv2
image = cv2.imread("testtt.png")
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml")
# detect all the faces in the image
faces = face_cascade.detectMultiScale(image_gray,1.1,5)
# print the number of faces detected
print("{len(faces)} faces detected in the image.")
for x, y, width, height in faces:
    cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
cv2.imwrite("face_detected.jpg", image)

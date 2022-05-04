import cv2
import imutils
# Face recognition classifier 
faceCascade = cv2.CascadeClassifier(
r"D:\PYcharm\PyCharm Community Edition 2020.3.3\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")
# Classifier for recognizing eyes 
eyeCascade = cv2.CascadeClassifier(
r'D:\MATLAB\mcr\toolbox\vision\visionutilities\classifierdata\cascade\haar\haarcascade_mcs_nose.xml')
# Turn on camera 
cap = cv2.VideoCapture(0)
ok = True
nosej=[" Left nostril "," Right nostril "]
center=[";","\n"]
while ok:
# Reading images from the camera ,ok It is used to judge whether the read is successful or not 
ok, img = cap.read()
img2 = img
# Convert the image to grayscale 
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# Face detection 
faces = faceCascade.detectMultiScale(
gray,
scaleFactor=1.2,
minNeighbors=15,
minSize=(32, 32)
)
# Eye detection based on face detection 
for (x, y, w, h) in faces:
fac_gray = gray[y: (y + h), x: (x + w)]
result = []
eyes = eyeCascade.detectMultiScale(fac_gray, 1.3, 5, cv2.CASCADE_SCALE_IMAGE, (40, 40), (80, 80))
for (ex, ey, ew, eh) in eyes:
# print(eyes[0])
result.append((x + ex, y + ey, ew, eh))
# print("www",result)
# Draw a rectangular 
for (x, y, w, h) in faces:
cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
try:
for (ex, ey, ew, eh) in result:
cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2) # nose 
img_eye_l = cv2.resize(img2[result[0][1]:result[0][1] + result[0][3], result[0][0]:result[0][0] + result[0][2]], (300, 300))
img_eye_l = img_eye_l[60:240, 10:290]
image = img_eye_l
image = cv2.resize(image, (image.shape[1], image.shape[0]))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Grayscale 
blurred = cv2.GaussianBlur(gray, (5, 5), 0) # 5x5 Gaussian smoothing of the kernel 
##################################
thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY_INV)[1] # Thresholding , After thresholding, the shape is represented as a white foreground on a black background .
############################# ↑ (1,74)
cv2.imshow("Image", thresh)
# Find the contour in the threshold image 
# Find the set of boundary points corresponding to white 
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# Calculate the contour center 
m=1
for c in cnts:
m+=1
n=m%2
M = cv2.moments(c)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
# Draw the outline and center of the shape on the image 
cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
cv2.putText(image, "center", (cX - 20, cY - 20),
cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
# Show pictures 
cv2.imshow("Image", image)
# with open(file_path, 'w') as w_obj:
# w_obj.write(str(cX) +' ' + str(cY)+ "\n")
cv2.waitKey(1)
# print(" Left nostril :", cX, " Right nostril :", cY)
print(" Coordinates relative to the nose ："f"{
nosej[n]}:"f"({
cX},{
cY})",end=center[0])
print(" Coordinates relative to the face ："f"{
nosej[n]}:"f"({
cX+x},{
cY+y})",end=center[0])
print(" Coordinates relative to the camera ："f"{
nosej[n]}:"f"({
cX + ex},{
cY + ey})", end=center[1])
except:
pass
cv2.imshow('video', img)
k = cv2.waitKey(1)
if k == 27:
break
cap.release()
cv2.destroyAllWindows()


"""
ECE196 Face Recognition Project
Author: W Chen

Adapted from:
http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

Use this code as a template to process images in real time, using the same techniques as the last challenge.
You need to display a gray scale video with 320x240 dimensions, with box at the center
"""


# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

haarcascade_frontalface = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
haarcascade_eye = "/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml"

face_cascade = cv.CascadeClassifier(haarcascade_frontalface)
eye_cascade = cv.CascadeClassifier(haarcascade_eye)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    cv.flip(image, 0)

    height, width, channel = image.shape

    factor = 2

    grayimage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    grayimage = cv.resize(grayimage, (round(height/factor), round(width/factor)))


    

    faces = face_cascade.detectMultiScale(grayimage, 1.2, 5)

    for (x,y,w,h) in faces:
        cv.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = grayimage[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 5)
        for (ex,ey,ew,eh) in eyes:
            cv.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)


    # show the frame
    cv.imshow("Frame", image)
    key = cv.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


cv.destroyAllWindows()

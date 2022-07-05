from __future__ import print_function
from linecache import getline
import sys
import numpy as np
import pyzed.sl as sl
import cv2
import argparse
import json

zed = sl.Camera()

# Set configuration parameters
input_type = sl.InputType()
if len(sys.argv) >= 2 :
    input_type.set_from_svo_file(sys.argv[1])
    

init = sl.InitParameters(input_t=input_type)
init.camera_resolution = sl.RESOLUTION.VGA
init.camera_fps = 100

err = zed.open(init)

zed.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, 50)
zed.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, 85)
zed.set_camera_settings(sl.VIDEO_SETTINGS.GAMMA, 6)
zed.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, 8)
zed.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION,5)
zed.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, 8)
zed.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, 2)
zed.set_camera_settings(sl.VIDEO_SETTINGS.HUE, 0)


max_value = 255
max_value_H = 360//2
low_H = 50
low_S = 93
low_V = 149
high_H = 96
high_S = 255
high_V = 255
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
color_yellow = (0,255,255)


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_detection_name)
cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar) 


# Open the camera

if err != sl.ERROR_CODE.SUCCESS :
    print(repr(err))
    zed.close()
    exit(1)

# Set runtime parameters after opening the camera
runtime = sl.RuntimeParameters()
runtime.sensing_mode = sl.SENSING_MODE.STANDARD

# Prepare new image size to retrieve half-resolution images
image_size = zed.get_camera_information().camera_resolution

# Declare your sl.Mat matrices
image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)


S_full = image_size.width * image_size.height
S_ball = 0.001256
S_0 = 1.838
dist0 = 0.75
points = []



key = ''
for i in range(500):

    err = zed.grab(runtime)
    if err == sl.ERROR_CODE.SUCCESS :
        zed.retrieve_image(image_zed, sl.VIEW.LEFT, sl.MEM.CPU, image_size)
        image_ocv = image_zed.get_data()
        

        hsv_min = np.array((low_H, low_S, low_V), np.uint8)
        hsv_max = np.array((high_H, high_S, high_V), np.uint8)
        hsv = cv2.cvtColor(image_ocv, cv2.COLOR_BGR2HSV )
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)
        cv2.imshow(window_detection_name, thresh)

        
        
        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if dArea > 30:
            x = int(dM10 / dArea - (image_size.width / 2))
            y = int(dM01 / dArea - (image_size.height / 2))


            cv2.circle(image_ocv, (x+336, y+188), 5, color_yellow, 2)
            cv2.putText(image_ocv, "%d-%d" % (x,y), (x+346,y+178), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

            pix_size = (S_ball / dArea) ** 0.5
            points.append((x * pix_size, y * pix_size, (dist0 * ((S_full * S_ball) / (dArea * S_0)) ** 0.5)))
            print(points[-1])

        cv2.imshow(window_capture_name, image_ocv)

        key = cv2.waitKey(10)

with open("data.json", "w") as file:
    json.dump(points, file)    
    
cv2.destroyAllWindows()
zed.close()

print("\nFINISH")


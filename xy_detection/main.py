from __future__ import print_function
from linecache import getline
import sys
import numpy as np
import pyzed.sl as sl
import cv2
import argparse
import json
from config import Config
from cameraConfig import Camera


zed = Camera()

runtime = sl.RuntimeParameters()
runtime.sensing_mode = sl.SENSING_MODE.STANDARD

image_size = zed.device.get_camera_information().camera_resolution


image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4) 


S_full = image_size.width * image_size.height
S_ball = 0.001256
S_0 = 1.838
dist0 = 1.27
points = []



key = ''
while True:

    err = zed.device.grab(runtime)
    if err == sl.ERROR_CODE.SUCCESS :
        zed.device.retrieve_image(image_zed, sl.VIEW.LEFT, sl.MEM.CPU, image_size)
        image_ocv = image_zed.get_data()
        undistorted = cv2.undistort(image_ocv, zed.mtx, zed.dist, None, zed.upd_camera_matrix)
        x, y, w, h = zed.rect
        undistorted = undistorted[y:y+h, x:x+w]

        

        hsv_min = np.array((zed.config.low_H, zed.config.low_S, zed.config.low_V), np.uint8)
        hsv_max = np.array((zed.config.high_H, zed.config.high_S, zed.config.high_V), np.uint8)
        hsv = cv2.cvtColor(undistorted, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)


        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if dArea > 20:
            x = int(dM10 / dArea - (image_size.width / 2))
            y = int(dM01 / dArea - (image_size.height / 2))


            cv2.circle(image_ocv, (x+336, y+188), 5, zed.config.color_yellow, 2)
            cv2.putText(image_ocv, "%d-%d" % (x,y), (x+346,y+178), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, zed.config.color_yellow, 2)

            pix_size = (S_ball / dArea) ** 0.5
            points.append((x * pix_size, y * pix_size, (dist0 * ((S_full * S_ball) / (dArea * S_0)) ** 0.5)))
            print(points[-1])


        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGRA)
        cv2.imshow(zed.config.window_capture_name, np.concatenate((undistorted, thresh), axis = 1))
        print()
        print(undistorted.shape)
        print()
        key = cv2.waitKey(10)

with open("data.json", "w") as file:
    json.dump(points, file)    
    
cv2.destroyAllWindows()
zed.device.close()

print("\nFINISH")


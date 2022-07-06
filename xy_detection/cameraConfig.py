import pyzed.sl as sl
import sys
from config import Config
import cv2
import numpy as np
import time

class Camera():
    def __init__(self):
        self.device = sl.Camera()
        self.config = Config()

        input_type = sl.InputType()
        if len(sys.argv) >= 2 :
            input_type.set_from_svo_file(sys.argv[1])
    
        init = sl.InitParameters(input_t=input_type)
        init.camera_resolution = sl.RESOLUTION.VGA
        init.camera_fps = 100

        self.device.open(init)
        self.update_device_config()

        self.camera_window()
        self.camera_window_mask()

    def update_device_config(self):
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, self.config.camera_exposure)
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, self.config.camera_gain)
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.GAMMA, self.config.camera_gamma)
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, self.config.camera_sharpness)
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION,self.config.camera_saturation)
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, self.config.camera_contrast)
        self.device.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, self.config.camera_brightness)


    def camera_window(self):
        def exposure_trackbar(val):
            self.config.camera_exposure = val
            cv2.setTrackbarPos(self.config.camera_exposure_name, self.config.window_capture_name, self.config.camera_exposure)
            self.update_device_config()
        def gain_trackbar(val):
            self.config.camera_gain = val
            cv2.setTrackbarPos(self.config.camera_gain_name, self.config.window_capture_name, self.config.camera_gain)
            self.update_device_config()
        def gamma_trackbar(val):
            self.config.camera_gamma = val
            cv2.setTrackbarPos(self.config.camera_gamma_name, self.config.window_capture_name, self.config.camera_gamma)
            self.update_device_config()
        def sharpness_trackbar(val):
            self.config.camera_sharpness = val
            cv2.setTrackbarPos(self.config.camera_sharpness_name, self.config.window_capture_name, self.config.camera_sharpness)
            self.update_device_config()
        def saturation_trackbar(val):
            self.config.camera_saturation = val
            cv2.setTrackbarPos(self.config.camera_saturation_name, self.config.window_capture_name, self.config.camera_saturation)
            self.update_device_config()
        def contrast_trackbar(val):
            self.config.camera_contrast = val
            cv2.setTrackbarPos(self.config.camera_contrast_name, self.config.window_capture_name, self.config.camera_contrast)
            self.update_device_config()
        def brightness_trackbar(val):
            self.config.camera_brightness = val
            cv2.setTrackbarPos(self.config.camera_brightness_name, self.config.window_capture_name, self.config.camera_brightness)
            self.update_device_config()

        cv2.namedWindow(self.config.window_capture_name)

        cv2.createTrackbar(self.config.camera_exposure_name, self.config.window_capture_name , self.config.camera_exposure, 100, exposure_trackbar)
        cv2.createTrackbar(self.config.camera_gain_name, self.config.window_capture_name , self.config.camera_gain, 100, gain_trackbar)
        cv2.createTrackbar(self.config.camera_gamma_name, self.config.window_capture_name , self.config.camera_gamma, 9, gamma_trackbar)
        cv2.createTrackbar(self.config.camera_sharpness_name, self.config.window_capture_name , self.config.camera_sharpness, 8, sharpness_trackbar)
        cv2.createTrackbar(self.config.camera_saturation_name, self.config.window_capture_name , self.config.camera_saturation, 8, saturation_trackbar)
        cv2.createTrackbar(self.config.camera_contrast_name, self.config.window_capture_name , self.config.camera_contrast, 8, contrast_trackbar)
        cv2.createTrackbar(self.config.camera_brightness_name, self.config.window_capture_name , self.config.camera_brightness, 8, brightness_trackbar)

        cv2.namedWindow(self.config.window_capture_name)

    def camera_window_mask(self):
        def on_low_H_thresh_trackbar(val):
            self.config.low_H = val
            self.config.low_H = min(self.config.high_H-1, self.config.low_H)
            cv2.setTrackbarPos(self.config.low_H_name, self.config.window_capture_name, self.config.low_H)
        def on_high_H_thresh_trackbar(val):
            self.config.high_H = val
            self.config.high_H = max(self.config.high_H, self.config.low_H+1)
            cv2.setTrackbarPos(self.config.high_H_name, self.config.window_capture_name, self.config.high_H)
        def on_low_S_thresh_trackbar(val):
            self.config.low_S = val
            self.config.low_S = min(self.config.high_S-1, self.config.low_S)
            cv2.setTrackbarPos(self.config.low_S_name, self.config.window_capture_name, self.config.low_S)
        def on_high_S_thresh_trackbar(val):
            self.config.high_S = val
            self.config.high_S = max(self.config.high_S, self.config.low_S+1)
            cv2.setTrackbarPos(self.config.high_S_name, self.config.window_capture_name, self.config.high_S)
        def on_low_V_thresh_trackbar(val):
            self.config.low_V = val
            self.config.low_V = min(self.config.high_V-1, self.config.low_V)
            cv2.setTrackbarPos(self.config.low_V_name, self.config.window_capture_name, self.config.low_V)
        def on_high_V_thresh_trackbar(val):
            self.config.high_V = val
            self.config.high_V = max(self.config.high_V, self.config.low_V+1)
            cv2.setTrackbarPos(self.config.high_V_name, self.config.window_capture_name, self.config.high_V)

        cv2.namedWindow(self.config.window_capture_name)
        cv2.createTrackbar(self.config.low_H_name, self.config.window_capture_name , self.config.low_H, self.config.max_value_H, on_low_H_thresh_trackbar)
        cv2.createTrackbar(self.config.high_H_name, self.config.window_capture_name , self.config.high_H, self.config.max_value_H, on_high_H_thresh_trackbar)
        cv2.createTrackbar(self.config.low_S_name, self.config.window_capture_name , self.config.low_S, self.config.max_value, on_low_S_thresh_trackbar)
        cv2.createTrackbar(self.config.high_S_name, self.config.window_capture_name , self.config.high_S, self.config.max_value, on_high_S_thresh_trackbar)
        cv2.createTrackbar(self.config.low_V_name, self.config.window_capture_name , self.config.low_V, self.config.max_value, on_low_V_thresh_trackbar)
        cv2.createTrackbar(self.config.high_V_name, self.config.window_capture_name , self.config.high_V, self.config.max_value, on_high_V_thresh_trackbar) 







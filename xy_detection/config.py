import dataclasses as dc
import pyzed.sl as sl

@dc.dataclass
class Config:
    #camera init
    camera_resolution = sl.RESOLUTION.VGA
    camera_fps = 100

    #camera settings
    camera_exposure = 26
    camera_gain = 56   
    camera_gamma = 8  
    camera_sharpness = 8   
    camera_saturation = 8   
    camera_contrast = 3  
    camera_brightness = 7     

    #camera mask settings
    max_value = 255
    max_value_H = 180
    low_H = 66
    low_S = 124
    low_V = 118
    high_H = 96
    high_S = 255
    high_V = 210

    #names
    window_capture_name = 'Video Capture'
    window_detection_name = 'Object Detection'
    low_H_name = 'Low H'
    low_S_name = 'Low S'
    low_V_name = 'Low V'
    high_H_name = 'High H'
    high_S_name = 'High S'
    high_V_name = 'High V'


    camera_exposure_name = 'camera_exposure'   
    camera_gain_name = 'camera_gain'   
    camera_gamma_name = 'camera_gamma'   
    camera_sharpness_name = 'camera_sharpness'   
    camera_saturation_name = 'camera_saturation'   
    camera_contrast_name = 'camera_contrast'   
    camera_brightness_name = 'camera_brightness'     


    #addings
    color_yellow = (0,255,255)



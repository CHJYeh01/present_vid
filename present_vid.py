# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np

def set_default_params():
    params = dict()
    params['vid_in'] = []#vid to be converted
    params['vid_out'] = []#name of converted vid
    params['fourcc'] = 'MJPG'
    params['fps'] = 25 #fps of output vid
    params['frame_scale'] = 1#scaling of frame output
    params['frame_interval'] = 1# frame interval to export to vid out
    params['start_time'] = 0 #start time of conversion
    params['timestamp'] = True
    params['timestamp_coord'] = (10, 100)
    params['timestamp_font'] = 0.5
    
    return params

def convert_vid(params):
    cap = cv2.VideoCapture(params['vid_in'])
    ow = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#original vid width
    oh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#original vid height
    frame_size = (int(ow*params['frame_scale']), int(oh*params['frame_scale']))
    print(frame_size)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(params['vid_out'], fourcc, params['fps'], frame_size)
    counter = 0 # starting counter for the while loop
    counter2 = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    converted_length = int(length / params['frame_interval'])
    
    
    while cap.isOpened():
        # print('test')
        ret, frame = cap.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)/1000#timestamp in s
    
                   
        if timestamp < params['start_time']:
            continue
        else:
            if np.mod(counter, params['frame_interval']) == 0:
                w = int(np.shape(frame)[1] * params['frame_scale'])
                h = int(np.shape(frame)[0] * params['frame_scale'])
                time_str = "{:.2f} s".format(timestamp)
                frame_out = cv2.resize(frame, (w, h))
                
                if params['timestamp'] == True:
                    frame_out = cv2.putText(frame_out, time_str,
                                params['timestamp_coord'],
                                font, params['timestamp_font'],
                                (255, 0, 0), 
                                1, 2)
                out.write(frame_out)
                
                frac = (counter2/converted_length) * 100
                print("converted {} out of {}, {}% finished".format(counter2, converted_length, frac))
                counter2 = counter2 + 1
        
        counter = counter + 1
            
            
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('done')
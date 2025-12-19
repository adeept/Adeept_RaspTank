#!/usr/bin/env python3
# coding: utf-8
import os
import cv2
from base_camera import BaseCamera
import RPIservo
import numpy as np
import move
import switch
import datetime
import Kalman_filter
import PID
import time
import threading
import imutils

import libcamera

from picamera2 import Picamera2, Preview
import io
# from threading import Condition, Thread, Event
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
# import robotLight

# led = robotLight.RobotLight()
pid = PID.PID()
pid.SetKp(0.5)
pid.SetKd(0)
pid.SetKi(0)

Threshold = 80 # 
findLineMove = 1
tracking_servo_status = 0
FLCV_Status = 0

CVRun = 1
linePos_1 = 440
linePos_2 = 380
lineColorSet = 255
frameRender = 1
findLineError = 20

# When turning, only one wheel pushes the car, so a value higher than forward_speed is required.
turn_speed = 45 # Range of values: 0-100
forward_speed = 20 # Avoid too fast, the video screen does not respond in time. Range of values: 0-100.


hflip = 0 # Video flip horizontally: 0 or 1 
vflip = 0 # Video vertical flip: 0/1 
ImgIsNone = 0

colorUpper = np.array([44, 255, 255])
colorLower = np.array([24, 100, 100])
APPMode = None

def map(input, in_min,in_max,out_min,out_max):
    return (input-in_min)/(in_max-out_min)*(out_max-out_min)+out_min

class CVThread(threading.Thread):
# class CVThread(Thread):
    font = cv2.FONT_HERSHEY_SIMPLEX

    kalman_filter_X =  Kalman_filter.Kalman_filter(0.01,0.1)
    kalman_filter_Y =  Kalman_filter.Kalman_filter(0.01,0.1)
    P_direction = -1
    T_direction = -1
    P_servo = 1 # Horizontal servo
    T_servo = 2 # Vertical servo
    P_anglePos = 0
    T_anglePos = 0
    cameraDiagonalW = 64
    cameraDiagonalH = 48
    videoW = 640
    videoH = 480
    Y_lock = 0
    X_lock = 0
    tor = 17

    scGear = RPIservo.ServoCtrl()
    scGear.moveInit()
    move.setup()

    def __init__(self, *args, **kwargs):
        self.CVThreading = 0
        self.CVMode = 'none'
        self.imgCV = None

        self.mov_x = None
        self.mov_y = None
        self.mov_w = None
        self.mov_h = None

        self.radius = 0
        self.box_x = None
        self.box_y = None
        self.drawing = 0

        self.findColorDetection = 0

        self.left_Pos1 = None
        self.right_Pos1 = None
        self.center_Pos1 = None

        self.left_Pos2 = None
        self.right_Pos2 = None
        self.center_Pos2 = None

        self.center = None
        
        self.tracking_servo_left = None
        self.tracking_servo_left_mark = 0
        self.tracking_servo_right_mark = 0
        self.servo_left_stop = 0
        self.servo_right_stop = 0

        super(CVThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

        self.avg = None
        self.motionCounter = 0
        self.lastMovtionCaptured = datetime.datetime.now()
        self.frameDelta = None
        self.thresh = None
        self.cnts = None

    def mode(self, invar, imgInput):
        self.CVMode = invar
        self.imgCV = imgInput
        self.resume()

    def elementDraw(self,imgInput):
        if self.CVMode == 'none':
            pass

        elif self.CVMode == 'findColor':
            if self.findColorDetection:
                cv2.putText(imgInput,'Target Detected',(40,60), CVThread.font, 0.5,(255,255,255),1,cv2.LINE_AA)
                self.drawing = 1
            else:
                cv2.putText(imgInput,'Target Detecting',(40,60), CVThread.font, 0.5,(255,255,255),1,cv2.LINE_AA)
                self.drawing = 0

            if self.radius > 10 and self.drawing:
                cv2.rectangle(imgInput,(int(self.box_x-self.radius),int(self.box_y+self.radius)),(int(self.box_x+self.radius),int(self.box_y-self.radius)),(255,255,255),1)

        elif self.CVMode == 'findlineCV':
            CVThread.scGear.moveAngle(2, -15) # The camera looks down.

            if frameRender:
                imgInput = cv2.cvtColor(imgInput, cv2.COLOR_BGR2GRAY)
                '''
                Image binarization, the method of processing functions can be searched for "threshold" in the link: http://docs.opencv.org/3.0.0/examples.html
                '''
                retval_bw, imgInput =  cv2.threshold(imgInput, Threshold, 255, cv2.THRESH_BINARY) # Set the threshold manually and set it to 80.
                imgInput = cv2.erode(imgInput, None, iterations=2) #  erode
                imgInput = cv2.dilate(imgInput, None, iterations=2) # dilate

            try:
                if lineColorSet == 255:
                    cv2.putText(imgInput,('Following White Line'),(30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(128,255,128),1,cv2.LINE_AA)
                else:
                    cv2.putText(imgInput,('Following Black Line'),(30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(128,255,128),1,cv2.LINE_AA)
                imgInput=cv2.merge((imgInput.copy(),imgInput.copy(),imgInput.copy()))
                cv2.line(imgInput,(self.left_Pos1,(linePos_1+30)),(self.left_Pos1,(linePos_1-30)),(255,128,64),2)
                cv2.line(imgInput,(self.right_Pos1,(linePos_1+30)),(self.right_Pos1,(linePos_1-30)),(64,128,255),2)
                cv2.line(imgInput,(0,linePos_1),(640,linePos_1),(255,128,64),1)

                cv2.line(imgInput,(self.left_Pos2,(linePos_2+30)),(self.left_Pos2,(linePos_2-30)),(64,128,255),2)
                cv2.line(imgInput,(self.right_Pos2,(linePos_2+30)),(self.right_Pos2,(linePos_2-30)),(64,128,255),2)
                cv2.line(imgInput,(0,linePos_2),(640,linePos_2),(64,128,255),1)

                cv2.line(imgInput,((self.center-20),int((linePos_1+linePos_2)/2)),((self.center+20),int((linePos_1+linePos_2)/2)),(0,0,0),1)
                cv2.line(imgInput,((self.center),int((linePos_1+linePos_2)/2+20)),((self.center),int((linePos_1+linePos_2)/2-20)),(0,0,0),1)

            except:
                pass

        elif self.CVMode == 'watchDog':
            if self.drawing:
                cv2.rectangle(imgInput, (self.mov_x, self.mov_y), (self.mov_x + self.mov_w, self.mov_y + self.mov_h), (128, 255, 0), 1)

        return imgInput


    def watchDog(self, imgInput):
        timestamp = datetime.datetime.now()
        gray = cv2.cvtColor(imgInput, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.avg is None:
            print("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")
            return 'background model'

        cv2.accumulateWeighted(gray, self.avg, 0.5)
        self.frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        self.thresh = cv2.threshold(self.frameDelta, 5, 255,
            cv2.THRESH_BINARY)[1]
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)
        self.cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = imutils.grab_contours(self.cnts)
        # loop over the contours
        for c in self.cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                continue
     
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (self.mov_x, self.mov_y, self.mov_w, self.mov_h) = cv2.boundingRect(c)
            self.drawing = 1
            
            self.motionCounter += 1
            self.lastMovtionCaptured = timestamp

        if (timestamp - self.lastMovtionCaptured).seconds >= 0.5:
            self.drawing = 0
        self.pause()


    def findLineCtrl(self, posInput):
        global findLineMove,tracking_servo_status,FLCV_Status
        
        if FLCV_Status == 0:    
            CVThread.scGear.moveAngle(0, 0) # car center. (servo_num, deflection angle)
            CVThread.scGear.moveAngle(1, 0) # camera centered. (servo_num, deflection angle)
            CVThread.scGear.moveAngle(2, 0)
            FLCV_Status = 1
        if posInput != None and findLineMove == 1:
            if FLCV_Status == -1:
                CVThread.scGear.stopWiggle()
                self.tracking_servo_left_mark = 0
                self.tracking_servo_right_mark = 0
                FLCV_Status = 1
            if posInput > 480: # The position of the center of the black line in the screen (value range: 0-640)
                tracking_servo_status = 1 #  right. -1/0/1: left/mid/right. In which direction the track may be offset out of the tracking area.
                if CVRun:
                    CVThread.scGear.moveAngle(0, -30) 
                    move.video_Tracking_Move(turn_speed, 1) 
                else:
                    CVThread.scGear.moveAngle(0, 0)
                    move.motorStop() # stop

            elif posInput < 180: # turnLeft.
                tracking_servo_status = -1 # left
                if CVRun:
                    CVThread.scGear.moveAngle(0, 30) 
                    move.video_Tracking_Move(turn_speed, 1) 
                
                else:
                    CVThread.scGear.moveAngle(0, 0)
                    move.motorStop() # stop.
                        
            else:
                tracking_servo_status = 0 # mid
                if CVRun:
                    CVThread.scGear.moveAngle(0, 0) 
                    move.video_Tracking_Move(turn_speed, 1) 

                else: 
                    move.motorStop() # stop
                pass
        
        else: # Tracking color not found.
            move.motorStop() # stop.
            FLCV_Status = -1
            if tracking_servo_status == -1 : # -1/0/1: left/mid/right. rotation left.
                CVThread.scGear.moveAngle(0, 30) 
                move.video_Tracking_Move(turn_speed, 1) 
            elif tracking_servo_status == 1 : # rotation right
                CVThread.scGear.moveAngle(0, -30) 
                move.video_Tracking_Move(turn_speed, 1) 
            else:  # no track ahead. tracking_servo_status==0
                pass



    def findlineCV(self, frame_image):
        frame_findline = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
        retval, frame_findline =  cv2.threshold(frame_findline, Threshold, 255, cv2.THRESH_BINARY) # Set the threshold manually and set it to 80.
        frame_findline = cv2.erode(frame_findline, None, iterations=2)
        frame_findline = cv2.dilate(frame_findline, None, iterations=2)
        colorPos_1 = frame_findline[linePos_1]
        colorPos_2 = frame_findline[linePos_2]
        
        try:
            lineColorCount_Pos1 = np.sum(colorPos_1 == lineColorSet)
            lineColorCount_Pos2 = np.sum(colorPos_2 == lineColorSet)

            lineIndex_Pos1 = np.where(colorPos_1 == lineColorSet)
            lineIndex_Pos2 = np.where(colorPos_2 == lineColorSet)

            # Roughly judge whether there is a color to track.
            if lineIndex_Pos1 !=[]:
                if abs(lineIndex_Pos1[0][-1] - lineIndex_Pos1[0][0]) > 500:
                    print("Tracking color not found")
                    findLineMove = 0    # No tracking color, stop moving
                else:
                    findLineMove = 1
            elif lineIndex_Pos2!= []:
                if abs(lineIndex_Pos2[0][-1] - lineIndex_Pos2[0][0]) > 500:
                    print("Tracking color not found")
                    findLineMove = 0
                else:
                    findLineMove = 1

            if lineColorCount_Pos1 == 0:
                lineColorCount_Pos1 = 1
            if lineColorCount_Pos2 == 0:
                lineColorCount_Pos2 = 1

            self.left_Pos1 = lineIndex_Pos1[0][1] # Is [1] instead of [0], in order to remove black/white edges that may appear on the far left
            self.right_Pos1 = lineIndex_Pos1[0][lineColorCount_Pos1-2]   # 

            self.center_Pos1 = int((self.left_Pos1+self.right_Pos1)/2)

            self.left_Pos2 =  lineIndex_Pos2[0][1]
            self.right_Pos2 = lineIndex_Pos2[0][lineColorCount_Pos2-2]
            self.center_Pos2 = int((self.left_Pos2+self.right_Pos2)/2)

            self.center = int((self.center_Pos1+self.center_Pos2)/2)
        except:
            self.center = None
            pass

        self.findLineCtrl(self.center)
        self.pause()


    def servoMove(ID, Dir, errorInput):
        if ID == 1:
            errorGenOut = CVThread.kalman_filter_X.kalman(errorInput)
            CVThread.P_anglePos += 0.15*(errorGenOut*Dir)*CVThread.cameraDiagonalW/CVThread.videoW

            if abs(errorInput) > CVThread.tor:
                CVThread.scGear.moveAngle(ID,CVThread.P_anglePos)
                CVThread.X_lock = 0
            else:
                CVThread.X_lock = 1
        elif ID == 2:
            errorGenOut = CVThread.kalman_filter_Y.kalman(errorInput)
            CVThread.T_anglePos += 0.1*(errorGenOut*Dir)*CVThread.cameraDiagonalH/CVThread.videoH

            if abs(errorInput) > CVThread.tor:
                CVThread.scGear.moveAngle(ID,CVThread.T_anglePos)
                CVThread.Y_lock = 0
            else:
                CVThread.Y_lock = 1
        else:
            print('No servoPort %d assigned.'%ID)
        time.sleep(0.1)

    def findColor(self, frame_image):
        global APPMode
        if APPMode == 'APP':
            hsv = cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB)
        else:
            hsv = cv2.cvtColor(frame_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorLower, colorUpper)#1
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            self.findColorDetection = 1
            c = max(cnts, key=cv2.contourArea)
            ((self.box_x, self.box_y), self.radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            X = int(self.box_x)
            Y = int(self.box_y)
            error_Y = 240 - Y
            error_X = 320 - X
            CVThread.servoMove(CVThread.P_servo, CVThread.P_direction, -error_X)
            CVThread.servoMove(CVThread.T_servo, CVThread.T_direction, -error_Y)

        else:
            self.findColorDetection = 0
        self.pause()


    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def run(self):
        while 1:
            self.__flag.wait()
            if self.CVMode == 'none':
                continue
            
            elif self.CVMode == 'findColor':
                self.CVThreading = 1
                self.findColor(self.imgCV)
                self.CVThreading = 0
            elif self.CVMode == 'findlineCV':
                self.CVThreading = 1
                self.findlineCV(self.imgCV)
                self.CVThreading = 0
            elif self.CVMode == 'watchDog':
                self.CVThreading = 1
                self.watchDog(self.imgCV)
                self.CVThreading = 0
            else:
                pass




class Camera(BaseCamera):
    video_source = 0
    modeSelect = 'none'


    def colorFindSet(self, invarH, invarS, invarV):
        global colorUpper, colorLower
        HUE_1 = invarH+15
        HUE_2 = invarH-15
        if HUE_1>180:HUE_1=180
        if HUE_2<0:HUE_2=0

        SAT_1 = invarS+150
        SAT_2 = invarS-150
        if SAT_1>255:SAT_1=255
        if SAT_2<0:SAT_2=0

        VAL_1 = invarV+150
        VAL_2 = invarV-150
        if VAL_1>255:VAL_1=255
        if VAL_2<0:VAL_2=0

        colorUpper = np.array([HUE_1, SAT_1, VAL_1])
        colorLower = np.array([HUE_2, SAT_2, VAL_2])
        print('HSV_1:%d %d %d'%(HUE_1, SAT_1, VAL_1))
        print('HSV_2:%d %d %d'%(HUE_2, SAT_2, VAL_2))
        print(colorUpper)
        print(colorLower)

    def colorFindSetApp(self, invarH, invarS, invarV):
        global colorUpper, colorLower
        HUE_1 = invarH + 100
        HUE_2 = invarH - 100
        if HUE_1>255:
            HUE_1=255
        if HUE_2<0:
            HUE_2=0

        SAT_1 = invarS + 100
        SAT_2 = invarS-100
        if SAT_1>255:
            SAT_1=255
        if SAT_2<0:
            SAT_2=0

        VAL_1 = invarV+100
        VAL_2 = invarV-100
        if VAL_1>255:
            VAL_1=255
        if VAL_2<0:
            VAL_2=0

        colorUpper = np.array([HUE_1, SAT_1, VAL_1])
        colorLower = np.array([HUE_2, SAT_2, VAL_2])
        print('HSV_1:%d %d %d'%(HUE_1, SAT_1, VAL_1))
        print('HSV_2:%d %d %d'%(HUE_2, SAT_2, VAL_2))
        print(colorUpper)
        print(colorLower)


    def modeSet(self, invar):
        Camera.modeSelect = invar

    def CVRunSet(self, invar):
        global CVRun
        CVRun = invar

    def linePosSet_1(self, invar):
        global linePos_1
        linePos_1 = invar

    def linePosSet_2(self, invar):
        global linePos_2
        linePos_2 = invar

    def colorSet(self, invar):
        global lineColorSet
        lineColorSet = invar

    def randerSet(self, invar):
        global frameRender
        frameRender = invar

    def errorSet(self, invar):
        global findLineError
        findLineError = invar

    def Threshold(self, value):
        global Threshold
        Threshold = value
        
    def ThresholdOK(self):
        global Threshold
        return Threshold

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source





# _______________________________________________________
    @staticmethod
    def frames():
        global ImgIsNone,hflip,vflip
        picam2 = Picamera2() 
        
        preview_config = picam2.preview_configuration
        preview_config.size = (640, 480)
        preview_config.format = 'RGB888'  # 'XRGB8888', 'XBGR8888', 'RGB888', 'BGR888', 'YUV420'
        preview_config.transform = libcamera.Transform(hflip=hflip, vflip=vflip)
        preview_config.colour_space = libcamera.ColorSpace.Sycc()
        preview_config.buffer_count = 4
        preview_config.queue = True

        if not picam2.is_open:
            raise RuntimeError('Could not start camera.')

        try:
            picam2.start()
        except Exception as e:
            print(f"\033[38;5;1mError:\033[0m\n{e}")
            print("\nPlease check whether the camera is connected well,  \
                  and disable the \"legacy camera driver\" on raspi-config")

        cvt = CVThread()
        cvt.start()

        while True:
            start_time = time.time()
            img = picam2.capture_array()

            if img is None:
                if ImgIsNone == 0:
                    print("--------------------")
                    print("\033[31merror: Unable to read camera data.\033[0m")
                    print("Use the command: \033[34m'sudo killall python3'\033[0m. Close the self-starting program webServer.py")
                    print("Press the keyboard keys \033[34m'Ctrl + C'\033[0m multiple times to exit the current program.")
                    print("--------Ctrl+C quit-----------")
                    ImgIsNone = 1
                continue
            
            if Camera.modeSelect == 'none':
                cvt.pause()
            else:
                if cvt.CVThreading:
                    pass
                else:
                    pass
                    cvt.mode(Camera.modeSelect, img)
                    cvt.resume()
                try:
                    pass
                    img = cvt.elementDraw(img)
                except:
                    pass

            if cv2.imencode('.jpg', img)[0]:
                yield cv2.imencode('.jpg', img)[1].tobytes()
            

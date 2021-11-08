import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

cap = cv2.VideoCapture(1)

_, frame = cap.read()
windowWidth = frame.shape[1]

def camera():
    while True:
        area_red = 0
        area_green = 0

        _, frame = cap.read()
        blurred_frame = cv2.medianBlur(frame, 15)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 30])
        upper_red = np.array([5, 255, 255])
        mask_red_1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([175, 100, 30])
        upper_red = np.array([180, 255, 255])
        mask_red_2 = cv2.inRange(hsv, lower_red, upper_red)

        lower_green = np.array([40, 100, 30])
        upper_green = np.array([80, 255, 255])

        mask_red = mask_red_1 + mask_red_2
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours_red) != 0:
            for contour in contours_red:
                area = cv2.contourArea(contour)
                if area > 8000:
                    cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
                    area_red = area

        if len(contours_green) != 0:
            for contour in contours_green:
                area = cv2.contourArea(contour)
                if area > 8000:
                    cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
                    area_green = area

        if area_red > area_green:
            if len(contours_red) != 0:
                c = max(contours_red, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                red_x_midpt = (x + x + w) / 2
                red_y_midpt = (y + y + h) / 2
                return [0, area_red, red_x_midpt]

        elif area_green > area_red:
            if len(contours_green) != 0:
                c = max(contours_green, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                green_x_midpt = (x + x + w) / 2
                green_y_midpt = (y + y + h) / 2
                return [1, area_green, green_x_midpt]

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

in1 = 24
in2 = 23
in3 = 7
in4 = 8
en1 = 25
en2 = 12
temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p1=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)

p1.start(50)
p2.start(50)

def right_slow():
    p1.ChangeDutyCycle(25)

def right_medium():
    p1.ChangeDutyCycle(50)

def right_fast():
    p1.ChangeDutyCycle(75)

def left_slow():
    p2.ChangeDutyCycle(25)

def left_medium():
    p2.ChangeDutyCycle(50)

def left_fast():
    p2.ChangeDutyCycle(75)

def back(tf):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    sleep(tf)
    stop()

def forward(tf):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    sleep(tf)
    stop()

def spin_left(tf):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    sleep(tf)
    stop()

def spin_right(tf):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    sleep(tf)
    stop()

def pivot_right(tf):
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    sleep(tf)
    stop()

def pivot_left(tf):
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    sleep(tf)
    stop()

def stop():
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def clean():
    GPIO.cleanup()


count = 0
# TODO: Make bot start only when button pressed
while count < 18:
    if camera()[0] == 0 and camera()[1] > 8000:
        if camera()[2] < windowWidth/3:
            forward(2)
            if count != 17:
                pivot_left(1)
            else:
                forward(2)
        else:
            while camera()[2] >= windowWidth/3:
                pivot_right(0.5)
            forward(2)
            if count != 17:
                pivot_left(1)
            else:
                forward(2)
        count += 1
    elif camera()[0] == 1 and camera()[1] > 8000:
        if camera()[2] > windowWidth/3*2:
            forward(2)
            pivot_right(1)
        else:
            while camera()[2] <= windowWidth/3*2:
                pivot_left(0.5)
            forward(2)
            pivot_right(1)
        count += 1
    else:
        pass
        # TODO: Add light sensor code
        # if light sensor senses orange line:
        #     pivot_right(1)
        # else:
        #     forward(1)

cap.release()
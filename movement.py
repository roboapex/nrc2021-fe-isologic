# SETUP

## Imports
import RPi.GPIO as GPIO          
from time import sleep

## Setting pins

### Right motor
in1 = 24
in2 = 23
en1 = 25

### Left motor
in3 = 7
in4 = 8
en2 = 12

## Initialisation

### Initialising pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

### 'Zero'ing motors
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

### Initialising Pulse-width modulation
p1=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)

### Initialising motor speed
p1.start(50)
p2.start(50)

# FUNCTIONS

## Speed

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

## Stright-line movement

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

## Turning

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

## Endings

def stop():
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def clean():
    GPIO.cleanup()
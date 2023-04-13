import time
import board
import serial
import picamera
import sys,select
import adafruit_adxl34x
i2c = board.I2C()
from threading import Timer
timeout=5
accelerometer = adafruit_adxl34x.ADXL345(i2c)
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
import picamera
ans=""

acceleration_old_x=-0.745
acceleration_old_y=-1.255
def detection(x,y):
    if((x-accelration_old_x>2)or(y-accelration_old_y>2)or(x-accelration_old_x<-2)or(y-accelration_old_y<-2)):
        acceleration_old=x
        return 1
    else:
        acceleration_old=x
        return 0
def send_sms():
    port.write(b'AT\r')
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write(b"AT+CMGF=1\r")
    print("Text Mode Enabled…")
    time.sleep(3)
    port.write(b'AT+CMGS="+919538183826"\r')
    link="https://www.google.com/maps/place/"
    msg = "Accident has occured at location "+link+"\n"
    print("sending message….")
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg+chr(26)))
    time.sleep(3)
    print("message sent…")
def video_record():
    with picamera.PiCamera() as camera:
        camera.resolution=(1080,480)
        camera.start_recording('my_video.h264')
        camera.wait_recording()
        time.sleep(5)
i=0    
while True:
    x,y,z=accelerometer.acceleration
    print("started %d",i)
    r=detection(x,y)
    if(r==1):
        print("Accident has happend Do you what to report for yes y no n:")
        t1=time.time()
        ans=input()
        t2=time.time()
        t=t1-t2
        print(t)
        if(t>5):
            send_sms()
            video_record()
        else:
            if((ans=="n") or (ans=="N")):
                i=i+1
            else:
                send_sms()
                video_record() 

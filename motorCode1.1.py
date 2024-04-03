import time
import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25
temp1=1

in3 = 17
in4 = 27
en2 = 22
temp2=1

sen1 = False
# TBD
sen1_pin = #TBD

GPIO.setmode(GPIO.BCM)
#Set up for the first motor
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

#Set up for the second motor
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2,1000)


p.start(25)
p2.start(25)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward R-Right turn L-Left turn l-low m-medium h-high e-exit")
print("\n")    

while(1):
    # Sensor Detection 
    if GPIO.input(sen1_pin):
        sen1 = True
        print("Object Detected")
    else:
        sen1 = False
    time.sleep(0.2)
  
    x=input()
    # Forward 
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
          
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
          
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'

      # Stop
    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        x='z'
      
      # Forward
    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp1=1
        x='z'
      # Backward
    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1=0
        x='z'
    # Right Turn
    elif x=='R':
        print("right turn")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    # Left Turn
    elif x=='L':
        print("left turn")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
  
    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        p2.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        p2.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        p2.ChangeDutyCycle(75)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
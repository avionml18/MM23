import time
import RPi.GPIO as GPIO          
from time import sleep

# Motor pin assignments for motor 1
in1 = 24
in2 = 23
en = 25
temp1=1

# Motor pin assignments for motor 2
in3 = 17
in4 = 27
en2 = 22
temp2=1

# Sensor initial state and GPIO pin (to be defined)
sen1 = False
sen1_pin = 19 
sen2 = False
sen2_pin = 20
sen3 = False
sen3_pin = 18
# Set up the Raspberry Pi GPIO pins
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for the first motor
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)  # Setup PWM with 1000Hz frequency

# Set up GPIO pins for the second motor
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p2 = GPIO.PWM(en2, 1000)  # Setup PWM with 1000Hz frequency


###
#GPIO.setup(sen1_pin, GPIO.OUT)

#GPIO.output(sen1_pin, GPIO.LOW)

###

# Start PWM with 25% duty cycle
p.start(25)
p2.start(25)

print("\nThe default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward R-Right turn L-Left turn l-low m-medium h-high e-exit\n")    

while True:
    """"
    # Sensor detection check
    if GPIO.input(0):
        sen1 = True
        print("Object Detected")
    else:
        sen1 = False
    time.sleep(0.2)

    if GPIO.input(0):
        sen2 = True
        print("Object Detected")
    else:
        sen2 = False
    time.sleep(0.2)

    if GPIO.input(0):
        sen3 = True
        print("Object Detected")
    else:
        sen3 = False
    time.sleep(0.2)
  """
    x = input()
    if x == 'r':
        print("run")
        if temp1 == 1:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            print("forward")
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            print("backward")

    elif x == 's':
        print("stop")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

    elif x == 'f':
        print("forward")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        temp1 = 1

    elif x == 'b':
        print("backward")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        temp1 = 0

    elif x == 'R':
        print("right turn")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)

    elif x == 'L':
        print("left turn")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    elif x == 'l':
        print("low")
        p.ChangeDutyCycle(25)
        p2.ChangeDutyCycle(25)

    elif x == 'm':
        print("medium")
        p.ChangeDutyCycle(50)
        p2.ChangeDutyCycle(50)

    elif x == 'h':
        print("high")
        p.ChangeDutyCycle(75)
        p2.ChangeDutyCycle(75)

    elif x == 'e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Test Sensor Readings
front = 19
right = 20
left = 18

GPIO.setup(front, GPIO.IN)
GPIO.setup(left, GPIO.IN)
GPIO.setup(right, GPIO.IN)

temp = 0
while True:
    temp += 1
    if not GPIO.input(front):
        print("Wall Forward")
    else:
        print("Forward Empty")

    if not GPIO.input(left):
        print("Wall Left")
    else:
        print("Left Empty")

    if not GPIO.input(right):
        print("Wall Right")
    else:
        print("Right Empty")

    if temp == 4:
        break

    time.sleep(5)

print("Unit Test Demo Complete")

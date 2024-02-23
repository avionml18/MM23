import RPi.GPIO as IO
import time

IO.setwarnings(False)

IO.setmode(IO.BCM)

print("Setting up")
IO.setup(12, IO.OUT) 
IO.setup(18, IO.OUT)

print("assigning")
f = IO.PWM(12, 100)
b = IO.PWM(18, 100)

f.start(0)
b.start(0)

print("Forward")
f.ChangeDutyCycle(100)
time.sleep(1)
f.stop()

print("Backward")
b.ChangeDutyCycle(100)
time.sleep(1)
b.stop()

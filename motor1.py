import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
forwardPin = 12
backwardPin = 18

# Set up the GPIO pins as outputs
GPIO.setup(forwardPin, GPIO.OUT)
GPIO.setup(backwardPin, GPIO.OUT)

def motor_forward(duration):
    """Spin the motor forward for the specified duration in seconds."""
    GPIO.output(forwardPin, GPIO.HIGH)  # Enable forward
    GPIO.output(backwardPin, GPIO.LOW)  # Disable backward
    time.sleep(duration)
    GPIO.output(forwardPin, GPIO.LOW)  # Disable forward

def motor_backward(duration):
    """Spin the motor backward for the specified duration in seconds."""
    GPIO.output(forwardPin, GPIO.LOW)  # Disable forward
    GPIO.output(backwardPin, GPIO.HIGH)  # Enable backward
    time.sleep(duration)
    GPIO.output(backwardPin, GPIO.LOW)  # Disable backward

try:
    # Rotate motor
    print("Rotating motor forward.")
    motor_forward(1)  # Rotate forward for 1 second

    print("Rotating motor backward.")
    motor_backward(1)  # Rotate backward for 1 second

finally:
    # Clean up GPIO to ensure a clean exit
    GPIO.cleanup()
    print("GPIO cleaned up and motor control script ended.")

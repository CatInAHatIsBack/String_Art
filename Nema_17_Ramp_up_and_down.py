from machine import Pin
import time

# Define the pin numbers for the TB6600 driver
STEP_PIN = 2  # Change this to the GPIO pin connected to the STEP input of the TB6600
DIR_PIN = 3   # Change this to the GPIO pin connected to the DIR input of the TB6600

# Set up the motor control pins
step_pin = Pin(STEP_PIN, Pin.OUT)
dir_pin = Pin(DIR_PIN, Pin.OUT)

# Function to rotate the motor with configurable parameters
def rotate_motor(num_steps, rotation_direction=1, acc_steps=1000, min_speed = 1500, max_speed=300, total_steps=10000):

    # Set the direction
    dir_pin.value(rotation_direction)

    ## check for off by one if total steps < acc_steps * 2 and total steps is odd

    uninteruppted_acceleration = True
    if total_steps < acc_steps * 2:
        uninteruppted_acceleration = False 
        acc_steps = total_steps / 2

    steps = 0
    speed = min_speed
    
    # Acceleration
    while speed > max_speed and steps < acc_steps:
        steps += 1
        speed = speed - (min_speed - max_speed) / acc_steps
        print(speed)
        step_pin.value(0)
        step_pin.value(1)
        time.sleep_us(int(speed))
        
    if uninteruppted_acceleration:
        speed = max_speed 

    # Constant speed
    while steps < total_steps - acc_steps and uninteruppted_acceleration:
        steps += 1
        step_pin.value(0)
        step_pin.value(1)
        time.sleep_us(int(speed)) 
        

    # Deceleration
    while speed > min_speed and steps < total_steps:
        steps += 1
        speed = speed + (min_speed - max_speed) / acc_steps
        print(speed)
        step_pin.value(0)
        step_pin.value(1)
        time.sleep_us(int(speed))
    
# Set the number of steps and direction for rotation
num_steps = 9000  # Adjust this value based on your motor's specifications and your application
rotation_direction = 1  # 1 for clockwise, 0 for counterclockwise

# Rotate the motor with configurable parameters
rotate_motor(num_steps, rotation_direction,  acc_steps=1000, min_speed = 1500, max_speed=300, total_steps=10000)

# Cleanup GPIO
step_pin.value(0)
dir_pin.value(0)

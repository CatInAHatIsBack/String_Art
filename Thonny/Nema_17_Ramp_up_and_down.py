import math
import time


def simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees, fallAndRise, total_steps):
    delays = []
    start = time.ticks_ms()


    # Calculate the number of steps based on the degrees of rotation
    absSteps = round(abs(deltaS_degrees) / step_angle)

    # Define end point of acceleration and start point of deceleration
    s_1 = vmax * vmax / (2 * acc)
    s_2 = deltaS_degrees - s_1

    if s_1 > s_2:  # If we don't even reach full speed
        s_1 = deltaS_degrees / 2
        s_2 = deltaS_degrees / 2
        vmax = math.sqrt(deltaS_degrees * acc)

    for incStep in range(absSteps):
        # Calculate central position of current step in degrees
        s = (incStep + 0.5) * step_angle

        # Calculate velocity at current step
        if s < s_1:
            vcurr = math.sqrt(2 * s * acc)
        elif s < s_2:
            vcurr = vmax
        else:
            vcurr = math.sqrt(vmax * vmax - 2 * (s - s_2) * acc)

        # Convert velocity to delay
        tDelay = round(step_angle / vcurr * 1e6)  # in microseconds

        delays.append(tDelay)
    end = time.ticks_ms()
    time_diff = (end - start)

    print(end - start)
    print(end, start)
    return delays


# Example usage
step_angle = 360/1600  # step angle in degrees
vmax = 1600  # maximum velocity in degrees/s
acc = 1000   # acceleration in degrees/(s*s)
deltaS_degrees = 360*10
# total degrees of rotation
fallAndRise = True
total_steps = 1000


delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees, fallAndRise, total_steps)


from machine import Pin
import time

# Define the pin numbers for the TB6600 driver
STEP_PIN = 2  # Change this to the GPIO pin connected to the STEP input of the TB6600
DIR_PIN = 3   # Change this to the GPIO pin connected to the DIR input of the TB6600

# Set up the motor control pins
step_pin = Pin(STEP_PIN, Pin.OUT)
dir_pin = Pin(DIR_PIN, Pin.OUT)

# Function to rotate the motor with configurable parameters
def rotate_motor(num_steps, rotation_direction=1, acc_steps=1000, min_speed = 1500, max_speed=300, total_steps=2500):
    # res = []
    # Set the direction
    dir_pin.value(rotation_direction)

    ## check for off by one if total steps < acc_steps * 2 and total steps is odd
    res = 0
    # uninteruppted_acceleration = True
    # if total_steps < acc_steps * 2:
    #     uninteruppted_acceleration = False 
    #     acc_steps = total_steps / 2

    steps = 0
    # speed = min_speed
    # Acceleration
    for i in range(len(delays)):
    
        # steps += 1
        
        # res.append(speed)
        step_pin.value(0)
        step_pin.value(1)
        time.sleep_us(int(delays[i]))
        res+=1
    return res

# Set the number of steps and direction for rotation
num_steps = 9000  # Adjust this value based on your motor's specifications and your application
rotation_direction = 1  # 1 for clockwise, 0 for counterclockwise

# Rotate the motor with configurable parameters
res = rotate_motor(num_steps, rotation_direction,  acc_steps=1000, min_speed = 3000, max_speed=600, total_steps=10000)
print(res)
# with open('time_output.txt', 'w') as f:
#     for item in res:
#         f.write("%s\n" % item)

# Cleanup GPIO
step_pin.value(0)
dir_pin.value(0)
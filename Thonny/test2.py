import math
import time


def simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees):
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
            #print(1)
            vcurr = math.sqrt(2 * s * acc)
            
        elif s < s_2:
            #print(2)
            vcurr = vmax
        else:
            #print(3)
            #print(vmax, s, s_2, acc)
            sx = s - s_2
            #print(sx)
            vcurr = math.sqrt(vmax * vmax - 2 * (sx) * acc)
            #print(4)

        # Convert velocity to delay
        tDelay = round(step_angle / vcurr * 1e6)  # in microseconds

        delays.append(tDelay)
    end = time.ticks_ms()
    time_diff = (end - start)

    print(end - start)
    return delays


# Example usage
tot_nails = 300
tot_steps = 4500
nails=300

step_angle = 360/tot_steps  # step angle in degrees
vmax = 1012.5  # maximum velocity in degrees/s
acc = 1012.5   # acceleration in degrees/(s*s)
steps_nail = tot_steps / tot_nails
steps = steps_nail * nails
deltaS_degrees = step_angle * steps

# delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)


from machine import Pin
import time

# Define the pin numbers for the TB6600 driver
STEP_PIN = 2  # Change this to the GPIO pin connected to the STEP input of the TB6600
DIR_PIN = 3   # Change this to the GPIO pin connected to the DIR input of the TB6600

# Set up the motor control pins
step_pin = Pin(STEP_PIN, Pin.OUT)
dir_pin = Pin(DIR_PIN, Pin.OUT)

# Function to rotate the motor with configurable parameters
def rotate_motor(delays, rotation_direction=1):
    # Set the direction
    dir_pin.value(rotation_direction)

    ## check for off by one if total steps < acc_steps * 2 and total steps is odd
    res = 0
    # Acceleration
    for i in range(len(delays)):
        
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
# res = rotate_motor(num_steps, rotation_direction,  acc_steps=1000, min_speed = 3000, max_speed=600, total_steps=10000)
# print(res)


def get_dir_and_amount(left_value,right_value):
    total_nails = 300  # From 0 to 299

    closest_directions_updated = []
    x = []
    
    # Calculate the distance going left
    if left_value >= right_value:
        distance_left = left_value - right_value
    else:
        distance_left = left_value + (total_nails - right_value)

    # Calculate the distance going right
    if right_value >= left_value:
        distance_right = right_value - left_value
    else:
        distance_right = (total_nails - left_value) + right_value

    # Determine the closest direction
    # closest_direction = "left" if distance_left < distance_right else "right"
    closest_direction = 0 if distance_left < distance_right else 1 
    x.append(closest_direction)
    closest_directions_updated.append((left_value, right_value, closest_direction, distance_left, distance_right))

    #print(closest_directions_updated)
    #print(x)
    
    return(closest_direction, distance_left if closest_direction == 0 else distance_right)
    



    # for left_value, right_value in inp_nails:

    
    
def control(nails, direction=1):
    
    # Example usage
    tot_nails = 300
    tot_steps = 4500
    gr = 2.8125
    step_angle = 360/tot_steps  # step angle in degrees
    vmax = 360 * gr  # maximum velocity in degrees/s
    acc = 360 * gr  # acceleration in degrees/(s*s)
    steps_nail = tot_steps / tot_nails # steps per nail
    # steps = steps_nail * nails
    # deltaS_degrees = step_angle * steps

#     for left_value,right_value in inp_nails:
# 
#         rotation_direction, nails = get_dir_and_amount(left_value,right_value)  
#         half = int(steps_nail/2) 
#         total_steps = steps_nail * nails - half # - half to get to the middle of the nail
#         deltaS_degrees = step_angle * total_steps # total steps to degrees
#         
#         print(left_value,right_value) 
#         delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
#         res = rotate_motor(delays, rotation_direction)
#         ######## Hoook out ########
#         
#         deltaS_degrees = steps_nail 
#         
#         delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
#         res = rotate_motor(delays, rotation_direction)
#         ######## Hook in ########
#         
#         deltaS_degrees = half 
#         
#         delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
#         res = rotate_motor(delays, 0 if rotation_direction else 1)
        
        

    
#     for i in range(10):
#         if i % 2 == 0:
#             rotation_direction = 1
#         else:
#
    rotation_direction = direction 
    steps = steps_nail * nails #(i + 1)
    deltaS_degrees = step_angle * steps

    delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
    res = rotate_motor(delays, rotation_direction)






#inp_nails = [(0, 291), (291, 178), (178, 290), (290, 175), (175, 288), (288, 171), (171, 284), (284, 166), (166, 283), (283, 167), (167, 282), (282, 165), (165, 285), (285, 166), (166, 287), (287, 165), (165, 283), (283, 163), (163, 285), (285, 167), (167, 281), (281, 160), (160, 282), (282, 166), (166, 281), (281, 161)]

control(291,1)
control(178,0)
control(290,1)
control(175,0)
control(288,1)
control(171,0)
control(284,1)
control(166,0)
control(283,1)
control(167,0)
control(282,1)
control(165,0)
control(285,1)
control(166,0)
control(287,1)
control(165,0)

# Cleanup GPIO
step_pin.value(0)
dir_pin.value(0)

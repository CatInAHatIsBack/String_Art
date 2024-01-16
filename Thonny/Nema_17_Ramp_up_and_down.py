import math
import time
from machine import Pin, PWM
import utime

# Define the pin numbers for the TB6600 driver
STEP_PIN = 2
DIR_PIN = 3
DRILL_TOWER_STEP = 5
DRILL_TOWER_DIR = 6

# Set up the motor control pins
step_pin = Pin(STEP_PIN, Pin.OUT)
dir_pin = Pin(DIR_PIN, Pin.OUT)
drilltower_step_pin = Pin(DRILL_TOWER_STEP, Pin.OUT)
drilltower_dir_pin = Pin(DRILL_TOWER_DIR, Pin.OUT)

# Setup 
tot_nails = 300
tot_steps = 4500
step_per_nail =tot_steps/tot_nails
nails=300
lenght=5
drilltower_step_time_ms=300

step_angle = 360/tot_steps  # step angle in degrees
vmax = 360  # maximum velocity in degrees/s
acc = 360   # acceleration in degrees/(s*s)
steps_nail = tot_steps / tot_nails
steps = steps_nail * nails
deltaS_degrees = step_angle * steps
drilltower_deltaS_degrees=step_angle * step_per_nail
drill_deltaS_degrees=step_angle * step_per_nail

move_one = []




    
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
            vcurr = math.sqrt(2 * s * acc)
            
        elif s < s_2:
            vcurr = vmax
        else:
            sx = s - s_2
            vm2 = vmax * vmax
            sax = 2*sx*acc

            try:
                vcurr = math.sqrt(vm2 - sax)
            except:
                print(vcurr)

        # Convert velocity to delay
        if vcurr > 0:
            tDelay = round(step_angle / vcurr * 1e6)  # in microseconds
        else:
            tDelay = round(step_angle / vmax * 1e6)
        
            
        delays.append(tDelay)
    end = time.ticks_ms()
    time_diff = (end - start)
    return delays

def calculate_one():
    deltaS_degrees = steps_nail 
        
    move_one = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
    return move_one
move_one = calculate_one()



# Function to rotate the motor with configurable parameters
def rotate_motor(delays, rotation_direction=1):
    # Set the direction
    dir_pin.value(rotation_direction)

    #FOR Loop for delays
    for i in range(len(delays)):
        step_pin.value(0)
        step_pin.value(1)
        time.sleep_us(int(delays[i]))





# Function to rotate the motor with configurable parameters
def rotate_drilltower(dt_delays, time_ms=1000):
    # Set the direction
    dir_pin.value(1) 
    move_dt(0, dt_delays)
    time.sleep_ms(time_ms)
    move_dt(1, dt_delays)
        
    rotate_motor(move_one, 1)
    


def move_dt(pin_val, drilltower_delays):
    drilltower_dir_pin.value(pin_val)
    for i in range(len(drilltower_delays)):
            drilltower_step_pin.value(0)
            drilltower_step_pin.value(1)
            time.sleep_us(int(drilltower_delays[i]))



def get_dir_and_amount(tot_nails, left_value,right_value):

    closest_directions_updated = []
    x = []
    
    # Calculate the distance going left
    if left_value >= right_value:
        distance_left = left_value - right_value
    else:
        distance_left = left_value + (tot_nails - right_value)

    # Calculate the distance going right
    if right_value >= left_value:
        distance_right = right_value - left_value
    else:
        distance_right = (tot_nails - left_value) + right_value

    # Determine the closest direction
    # closest_direction = "left" if distance_left < distance_right else "right"
    closest_direction = 0 if distance_left < distance_right else 1 
    x.append(closest_direction)
    closest_directions_updated.append((left_value, right_value, closest_direction, distance_left, distance_right))
    
    return(closest_direction, distance_left if closest_direction == 0 else distance_right)





def control(inp_nails):
    
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

    for left_value,right_value in inp_nails:
        
        rotation_direction, nails = get_dir_and_amount(tot_nails,left_value,right_value)
        print(rotation_direction, nails, left_value, right_value)
        half = math.ceil(steps_nail/2)
        #print(half)
        total_steps = steps_nail * nails - half # - half to get to the middle of the nail
        deltaS_degrees = step_angle * total_steps # total steps to degrees
        
        #print(left_value,right_value) 
        delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
        res = rotate_motor(delays, rotation_direction)
        ######## Hoook out ########
        hooker(0)
        deltaS_degrees = steps_nail 
        
        delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
        res = rotate_motor(delays, rotation_direction)
        # ######## Hook in ########
        hooker(1)
        deltaS_degrees = half 
        
        delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
        res = rotate_motor(delays, 0 if rotation_direction else 1)
        
        
# def control(inp_nails,total_nails, steps_nail):
# 
#     for left_value,right_value in inp_nails:
#         
#         rotation_direction, nails = get_dir_and_amount(total_nails,left_value,right_value)
#         half = math.ceil(steps_nail/2)
#         total_steps = steps_nail * nails - half # - half to get to the middle of the nail
#         deltaS_degrees = step_angle * total_steps # total steps to degrees
#         
#         delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
#         rotate_motor(delays, rotation_direction)
#         ######## Hoook out ########
#         hooker(0)
#         deltaS_degrees = steps_nail 
#         
#         delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
#         rotate_motor(delays, rotation_direction)
#         # ######## Hook in ########
#         hooker(1)
#         deltaS_degrees = half 
#         
#         delays = simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees)
#         rotate_motor(delays, 0 if rotation_direction else 1)
        
        



def hooker(io):
    # Set the GPIO pin for the servo
    servo_pin = 4
    servo_pwm = PWM(Pin(servo_pin))

    # Set the PWM frequency (Hz) and duty cycle range (0-65535)
    pwm_freq = 50  # Hz
    pwm_min_range = 2700  
    pwm_max_range = 3300

    # Set up PWM on the servo pin
    servo_pwm.freq(pwm_freq)
    if io == 0:
        # Move from 0% to 100%
        for duty_cycle in range(pwm_max_range, pwm_min_range -1, -50):  # Adjust step size if needed
            servo_pwm.duty_u16(duty_cycle)
            utime.sleep_ms(20)  # Adjust this delay if needed
    else:
        # Move from 100% to 0%
        for duty_cycle in range(pwm_min_range, pwm_max_range+1, 50):  # Adjust step size if needed
            servo_pwm.duty_u16(duty_cycle)
            utime.sleep_ms(20)  # Adjust this delay if needed


inp_nails = [(0, 291), (291, 178), (178, 290), (290, 175), (175, 288), (288, 171), (171, 284), (284, 5), (5, 185), (185, 90), (90, 282), (282, 165), (165, 285), (285, 166), (166, 287), (287, 165), (165, 283), (283, 163), (163, 285), (285, 167), (167, 281), (281, 160), (160, 282), (282, 166), (166, 281), (281, 161)]

#control(inp_nails)


mov_per_rot = 1.5
rot_steps = 200 
num_rot = 3
total_move = rot_steps * mov_per_rot * num_rot

step_angle = 360/rot_steps  # step angle in degrees
vmax = 360  # maximum velocity in degrees/s
acc = 360   # acceleration in degrees/(s*s)
steps_move = tot_steps / tot_nails

drilltower_delays = simulate_stepper_motor(step_angle, vmax, acc, total_move)
for i in range(5):
    rotate_drilltower(drilltower_delays)

# Cleanup GPIO
step_pin.value(0)
dir_pin.value(0)

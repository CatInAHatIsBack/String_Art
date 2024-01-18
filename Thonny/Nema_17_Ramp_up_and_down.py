import math
import time
from machine import Pin, PWM
import utime

# Define the pin numbers for the TB6600 drivers
STEP_PIN = 2
DIR_PIN = 3
DRILL_TOWER_STEP = 5
DRILL_TOWER_DIR = 6

# Set up the motor control pins
step_pin = Pin(STEP_PIN, Pin.OUT)
dir_pin = Pin(DIR_PIN, Pin.OUT)
dt_step_pin = Pin(DRILL_TOWER_STEP, Pin.OUT)
dt_dir_pin = Pin(DRILL_TOWER_DIR, Pin.OUT)





# Setup rotary board
rb_tot_nails = 300
rb_tot_steps_per_rev = 4500
rb_nails=300
step_per_nail =rb_tot_steps_per_rev/rb_tot_nails

rb_step_angle = 360/rb_tot_steps_per_rev  # step angle in degrees
rb_vmax = 360  # maximum velocity in degrees/s
rb_acc = 360   # rb_acceleration in degrees/(s*s)
rb_steps_nail = rb_tot_steps_per_rev / rb_tot_nails
rb_nailsteps = rb_steps_nail * rb_nails
rb_deltaS_degrees = rb_step_angle * rb_nailsteps
rb_deltaS_degrees_one_nail = rb_step_angle * step_per_nail





#Setup Drilltower
dt_tot_steps_per_rev = 1600
dt_lenght = 8
dt_gr = 1 # 16/20
dt_threading = 1.5
dt_pausetime_ms = 1
dt_deltaS_degrees = rb_step_angle * step_per_nail

dt_step_angle = 360/dt_tot_steps_per_rev  # step angle in degrees
dt_vmax = 360  # maximum velocity in degrees/s
dt_acc = 360   # rb_acceleration in degrees/(s*s)
dt_steps = round(dt_lenght * dt_tot_steps_per_rev * dt_gr / dt_threading)
print(dt_steps)
dt_deltaS_degrees = dt_step_angle * dt_steps




def simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees):
    delays = []
    start = time.ticks_ms()


    # Calculate the number of steps based on the degrees of rotation
    absSteps = round(abs(deltaS_degrees) / step_angle)

    # Define end point of rb_acceleration and start point of deceleration
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
def drive_drilltower(dt_delays, pausetime_ms):
    # Set the direction
    dt_dir_pin.value(0)

    for i in range(len(dt_delays)):
        dt_step_pin.value(0)
        dt_step_pin.value(1)
        time.sleep_us(int(dt_delays[i]))
    
    time.sleep_ms(pausetime_ms)
    
    dt_dir_pin.value(1)
    
    for i in range(len(dt_delays)):
        dt_step_pin.value(0)
        dt_step_pin.value(1)
        time.sleep_us(int(dt_delays[i]))






def get_dir_and_amount(rb_tot_nails, left_value,right_value):

    closest_directions_updated = []
    x = []
    
    # Calculate the distance going left
    if left_value >= right_value:
        distance_left = left_value - right_value
    else:
        distance_left = left_value + (rb_tot_nails - right_value)

    # Calculate the distance going right
    if right_value >= left_value:
        distance_right = right_value - left_value
    else:
        distance_right = (rb_tot_nails - left_value) + right_value

    # Determine the closest direction
    # closest_direction = "left" if distance_left < distance_right else "right"
    closest_direction = 0 if distance_left < distance_right else 1 
    x.append(closest_direction)
    closest_directions_updated.append((left_value, right_value, closest_direction, distance_left, distance_right))
    
    return(closest_direction, distance_left if closest_direction == 0 else distance_right)





def control(inp_nails):
    
    # Example usage
    rb_tot_nails = 300
    rb_tot_steps_per_rev = 4500
    gr = 2.8125
    rb_step_angle = 360/rb_tot_steps_per_rev  # step angle in degrees
    rb_vmax = 360 * gr  # maximum velocity in degrees/s
    rb_acc = 360 * gr  # rb_acceleration in degrees/(s*s)
    rb_steps_nail = rb_tot_steps_per_rev / rb_tot_nails # steps per nail
    # steps = rb_steps_nail * rb_nails
    # rb_deltaS_degrees = rb_step_angle * steps

    for left_value,right_value in inp_nails:
        
        rotation_direction, rb_nails = get_dir_and_amount(rb_tot_nails,left_value,right_value)
        print(rotation_direction, rb_nails, left_value, right_value)
        half = math.ceil(rb_steps_nail/2)
        #print(half)
        total_steps = rb_steps_nail * rb_nails - half # - half to get to the middle of the nail
        rb_deltaS_degrees = rb_step_angle * total_steps # total steps to degrees
        
        #print(left_value,right_value) 
        rb_delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
        res = rotate_motor(rb_delays, rotation_direction)
        ######## Hoook out ########
        hooker(0)
        rb_deltaS_degrees = rb_steps_nail 
        
        rb_delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
        res = rotate_motor(rb_delays, rotation_direction)
        # ######## Hook in ########
        hooker(1)
        
        rb_deltaS_degrees = half 
        
        rb_delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
        res = rotate_motor(rb_delays, 0 if rotation_direction else 1)
        
        
# def control(inp_nails,total_nails, rb_steps_nail):
# 
#     for left_value,right_value in inp_nails:
#         
#         rotation_direction, rb_nails = get_dir_and_amount(total_nails,left_value,right_value)
#         half = math.ceil(rb_steps_nail/2)
#         total_steps = rb_steps_nail * rb_nails - half # - half to get to the middle of the nail
#         rb_deltaS_degrees = rb_step_angle * total_steps # total steps to degrees
#         
#         delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
#         rotate_motor(delays, rotation_direction)
#         ######## Hoook out ########
#         hooker(0)
#         rb_deltaS_degrees = rb_steps_nail 
#         
#         delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
#         rotate_motor(delays, rotation_direction)
#         # ######## Hook in ########
#         hooker(1)
#         rb_deltaS_degrees = half 
#         
#         delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
#         rotate_motor(delays, 0 if rotation_direction else 1)

def hole_control():
    dt_delays = simulate_stepper_motor(dt_step_angle, dt_vmax, dt_acc, dt_deltaS_degrees)
    drive_drilltower(dt_delays, dt_pausetime_ms)
    
    rb_delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees_one_nail)
    res = rotate_motor(rb_delays, 1)





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
for i in range(rb_tot_nails):
    hole_control()
    print(i)

# Cleanup GPIO
step_pin.value(0)
dir_pin.value(0)
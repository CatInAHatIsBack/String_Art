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
rb_gr = 2.8125
rb_tot_nails = 300
rb_tot_steps_per_rev = 1600 * rb_gr
rb_nails=300
step_per_nail =rb_tot_steps_per_rev/rb_tot_nails

rb_step_angle = 360/rb_tot_steps_per_rev  # step angle in degrees
rb_vmax = 360  # maximum velocity in degrees/s
rb_acc = 360   # rb_acceleration in degrees/(s*s)
rb_steps_per_nail = rb_tot_steps_per_rev / rb_tot_nails
rb_nailsteps_per_rotation = rb_steps_per_nail * rb_nails
rb_deltaS_degrees = rb_step_angle * rb_nailsteps_per_rotation




#Setup Drilltower
dt_tot_steps_per_rev = 1600
dt_lenght = 8
dt_gr = 1 # 16/20
dt_threading = 1.5
dt_pausetime_ms = 1

dt_step_angle = 360/dt_tot_steps_per_rev  # step angle in degrees
dt_vmax = 360  # maximum velocity in degrees/s
dt_acc = 360   # rb_acceleration in degrees/(s*s)
dt_steps = round(dt_lenght * dt_tot_steps_per_rev * dt_gr / dt_threading)
dt_deltaS_degrees = dt_step_angle * dt_steps

rb_vel_prof = []
dt_vel_prof = []


# https://hofmannu.org/2022/01/06/trap-vel-stepper-motor/
    
def simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees):
    # start = time.ticks_ms()

    accel = []

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
        if s < s_1: # accel phase
            vcurr = math.sqrt(2 * s * acc)
            accel.append( round(step_angle / vcurr * 1e6) )
        else:
            break
            
    # end = time.ticks_ms()
    # time_diff = (end - start)

    return accel

def get_vel_profiles():
    rb_vel_prof = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)
    dt_vel_prof = simulate_stepper_motor(dt_step_angle, dt_vmax, dt_acc, dt_deltaS_degrees)
    return rb_vel_prof, dt_vel_prof

rb_vel_prof, dt_vel_prof = get_vel_profiles()

def rb_steps_to_take( rb_nails ):
    return (rb_steps_per_nail * rb_nails)

def accel(pin, vel_prof, num_steps):
    # a = []
    for i in range(num_steps): # accel phase
        pin.value(0)
        pin.value(1)
        time.sleep_us(int(vel_prof[i]))
    #     a.append(int(vel_prof[i]))
    # return a
    
def const(pin, vel, num_steps):
    # c = []
    for i in range(num_steps): # accel phase
        pin.value(0)
        pin.value(1)
        time.sleep_us(int(vel)) 
        # c.append(vel)
    # return c
    
def decel(pin, vel_prof, num_steps):
    # d = []
    for i in range(num_steps): # accel phase
        pin.value(0)
        pin.value(1)
        time.sleep_us(int(vel_prof[num_steps -i -1]))
    #     d.append(int(vel_prof[num_steps -i -1]))
    # return d
            
    

def control_acc(pin, vel_prof, steps_to_next):
    # Determine the number of steps for each phase
    if steps_to_next <= len(vel_prof) * 2:
        # If we don't have enough steps for full accel and decel
        half_steps = int(steps_to_next // 2)
        accel_steps = int(half_steps)
        decel_steps = int(steps_to_next - half_steps)  # Adjust in case of odd total steps
        const_steps = 0
    else:
        # Full acceleration, constant, and deceleration phases
        accel_steps = len(vel_prof)
        decel_steps = len(vel_prof)
        const_steps = int(steps_to_next - (accel_steps + decel_steps))
         
    accel(pin, vel_prof, accel_steps)
    const(pin, vel_prof[accel_steps-1], const_steps)
    decel(pin, vel_prof, decel_steps)

    ## debuging
    # if len(d) != len(a):
    #     for i in range(len(a)):
    #         if a[i] != d[-i-1]:
    #             print("odd", i, a[i], d[-i-1])
    # else:
    #     for i in range(len(a)):
    #         if a[i] != d[-i-1]:
    #             print("even",i, a[i], d[-i-1])
           
        

    

# Function to rotate the motor with configurable parameters
def rotate_motor(steps_to_next, rotation_direction=1):
    # Set the direction
    dir_pin.value(rotation_direction)

    control_acc(step_pin, rb_vel_prof, steps_to_next)
         
    return
    


# Function to rotate the motor with configurable parameters
def rotate_drilltower(time_ms=1000):
    
    dt_dir_pin.value(0)
    control_acc(dt_step_pin, dt_vel_prof, dt_steps)
    time.sleep_ms(time_ms)
    dt_dir_pin.value(1)
    control_acc(dt_step_pin, dt_vel_prof, dt_steps)


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
    closest_direction = 0 if distance_left < distance_right else 1 
    
    return(closest_direction, distance_left if closest_direction == 0 else distance_right)


def control(inp_nails):

    for left_value,right_value in inp_nails:
        
        rotation_direction, to_next = get_dir_and_amount(rb_tot_nails,left_value,right_value)
        # print(rotation_direction, to_next, left_value, right_value)
        half = math.ceil(rb_steps_per_nail/2)

        steps_to_take = rb_steps_to_take(to_next) - half # - half to get to the middle of the nail
        
        res = rotate_motor(steps_to_take, rotation_direction)
        ######## Hoook out ########
        hooker(0)
        
        res = rotate_motor(rb_steps_per_nail, rotation_direction)
        # ######## Hook in ########
        hooker(1)

        if rb_steps_per_nail % 2 != 0:
            steps_to_take = half -1
 
        res = rotate_motor(steps_to_take, not rotation_direction)
        
        

def hole_control():
    rotate_drilltower(dt_pausetime_ms)
    res = rotate_motor(rb_steps_per_nail, 1)





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
# inp_nails = [ (281, 161)]

# control(inp_nails)

for i in range(rb_tot_nails):
    hole_control()
    print(i)

# Cleanup GPIO
step_pin.value(0)
dir_pin.value(0)
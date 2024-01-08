from machine import Pin, PWM
import utime

# Set the GPIO pin for the servo
servo_pin = 4
servo_pwm = PWM(Pin(servo_pin))

# Set the PWM frequency (Hz) and duty cycle range (0-65535)
pwm_freq = 50  # Hz
pwm_min_range = 2700  
pwm_max_range = 3500

# Set up PWM on the servo pin
servo_pwm.freq(pwm_freq)

# Move from 0% to 100%
for duty_cycle in range(pwm_max_range, pwm_min_range -1, -50):  # Adjust step size if needed
    servo_pwm.duty_u16(duty_cycle)
    utime.sleep_ms(20)  # Adjust this delay if needed

# Move from 100% to 0%
for duty_cycle in range(pwm_min_range, pwm_max_range+1, 50):  # Adjust step size if needed
    servo_pwm.duty_u16(duty_cycle)
    utime.sleep_ms(20)  # Adjust this delay if needed

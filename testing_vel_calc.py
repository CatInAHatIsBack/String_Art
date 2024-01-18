import math
import time

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np

gr = 2.8125
rb_tot_nails = 300
rb_tot_steps_per_rev = 1600*gr

step_per_nail =rb_tot_steps_per_rev/rb_tot_nails

rb_step_angle = 360/rb_tot_steps_per_rev  # step angle in degrees
rb_vmax = 360  # maximum velocity in degrees/s
rb_acc = 360   # rb_acceleration in degrees/(s*s)
rb_steps_nail = rb_tot_steps_per_rev / rb_tot_nails
rb_nailsteps = rb_steps_nail * rb_tot_nails
rb_deltaS_degrees = rb_step_angle * rb_nailsteps
rb_deltaS_degrees_one_nail = rb_step_angle * step_per_nail


def simulate_stepper_motor(step_angle, vmax, acc, deltaS_degrees):
    delays = []
    # start = time.ticks_ms()


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
    # end = time.ticks_ms()
    # time_diff = (end - start)
    return delays


delays = simulate_stepper_motor(rb_step_angle, rb_vmax, rb_acc, rb_deltaS_degrees)

# Convert delays from microseconds to milliseconds
delays_ms = np.array(delays) / 1000

# Calculate steps per millisecond
steps_per_ms = 1 / delays_ms

print(f'min delay: {min(delays)}')
print(f'max delay: {max(delays)}')


cumulative_time = np.cumsum(delays)
speeds = 1 / np.array(delays)


# Calculating changes in speed and time
delta_speeds = np.diff(speeds)  # Change in speed between each step
delta_time = np.diff(cumulative_time) / 1000  # Change in time between each step in seconds

# Calculating acceleration (change in speed over change in time)
acceleration = delta_speeds / delta_time

# To plot acceleration, we need to align it with the appropriate time. We'll use the midpoint between each time interval.
midpoints_time = (cumulative_time[:-1] + cumulative_time[1:]) / 2

# Calculating changes in steps and time
delta_steps = np.diff(steps_per_ms)  # Change in steps between each step
delta_time = np.diff(cumulative_time) / 1000  # Change in time between each step in seconds

# To plot steps, we need to align it with the appropriate time. We'll use the midpoint between each time interval.
midpoints_time = (cumulative_time[:-1] + cumulative_time[1:]) / 2



# Create the plot for acceleration vs. time using Plotly
fig = go.Figure()

# Add trace for acceleration vs. midpoints time
fig.add_trace(
    go.Scatter(x=midpoints_time, y=acceleration, mode='markers', name='Acceleration',
               marker=dict(color='green', size=3, line=dict(width=0.5, color='DarkSlateGrey')))
)
# fig.add_trace(
#     go.Scatter(x=midpoints_time, y=steps_per_ms[1:], mode='markers', name='Steps per ms',
#                marker=dict(color='green', size=3, line=dict(width=0.5, color='DarkSlateGrey')))
# )

# Update layout
fig.update_layout(
    title="Stepper Motor Acceleration vs. Time",
    xaxis_title="Time (ms)",
    yaxis_title="Acceleration (speed change per second)",
    template="plotly_white",
)

# # Update layout
# fig.update_layout(
#     title="Stepper Motor Steps vs. Time",
#     xaxis_title="Time (ms)",
#     yaxis_title="Steps per millisecond",
#     template="plotly_white",
# )
# Show the plot
pio.show(fig)

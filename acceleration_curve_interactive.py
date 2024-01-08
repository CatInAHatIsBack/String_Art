import matplotlib.pyplot as plt
import numpy as np


with open('time_output.txt', 'r') as f:
    delays = [float(line.strip()) for line in f]


import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np


with open('time_output.txt', 'r') as f:
    delays = [float(line.strip()) for line in f]
    
cumulative_time = np.cumsum(delays)
speeds = 1 / np.array(delays)


# Calculating changes in speed and time
delta_speeds = np.diff(speeds)  # Change in speed between each step
delta_time = np.diff(cumulative_time) / 1000  # Change in time between each step in seconds

# Calculating acceleration (change in speed over change in time)
acceleration = delta_speeds / delta_time

# To plot acceleration, we need to align it with the appropriate time. We'll use the midpoint between each time interval.
midpoints_time = (cumulative_time[:-1] + cumulative_time[1:]) / 2

# Create the plot for acceleration vs. time using Plotly
fig = go.Figure()

# Add trace for acceleration vs. midpoints time
fig.add_trace(
    go.Scatter(x=midpoints_time, y=acceleration, mode='markers', name='Acceleration',
               marker=dict(color='green', size=3, line=dict(width=0.5, color='DarkSlateGrey')))
)

# Update layout
fig.update_layout(
    title="Stepper Motor Acceleration vs. Time",
    xaxis_title="Time (ms)",
    yaxis_title="Acceleration (speed change per second)",
    template="plotly_white",
)

# Show the plot
pio.show(fig)
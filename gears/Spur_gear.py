import math
def gear_ratio(big_gear_angle,small_gear_angle,small_gear_teeth):
    #Gear Ratio= Desired Angle of Larger Gear/Step Angle of Smaller Gear
    ratio = big_gear_angle/small_gear_angle
    inverted = 1/ratio
    big_gear_teeth = inverted * small_gear_teeth
    return ratio, inverted, big_gear_teeth

steps_per_rotation = 512
angle_per_step = 360/steps_per_rotation
print(f"angle per step:{angle_per_step}")


big_gear_angle = .25
small_gear_angle = angle_per_step
small_gear_teeth = 48
ratio, inverted, big_gear_teeth = gear_ratio(big_gear_angle,small_gear_angle,small_gear_teeth)
print(ratio, inverted, big_gear_teeth)

print(f"angle big gear per step {angle_per_step * ratio}")

import plotly.graph_objects as go
import numpy as np

def calculate_nails_and_angles_plotly(radius, min_spacing, max_spacing, step):
    spacings = np.arange(min_spacing, max_spacing, step)
    num_nails = []
    angles = []

    circ = 2 * np.pi * radius
    print(circ)
    for spacing in spacings:
        max_nails = int(circ // spacing)
        angle = 360 / max_nails if max_nails > 0 else 0
        num_nails.append(max_nails)
        angles.append(angle)

    return num_nails, angles

# Plotting function for nails vs. angle using Plotly
def plot_nails_vs_angle_plotly(num_nails, angles):
    fig = go.Figure(data=go.Scatter(x=num_nails, y=angles, mode='markers', 
                                    marker=dict(size=8, color='blue'), 
                                    hoverinfo='all'))
    
    fig.update_layout(title='Number of Nails vs. Angle Between Nails',
                      xaxis_title='Number of Nails',
                      yaxis_title='Angle Between Nails (degrees)',
                      showlegend=False)
    fig.show()

# Example usage
radius = 29  # radius of the board
min_spacing = .1  # minimum spacing between nails
max_spacing = 2    # maximum spacing between nails
step = 0.1         # increment step for spacing

num_nails, angles = calculate_nails_and_angles_plotly(radius, min_spacing, max_spacing, step)
plot_nails_vs_angle_plotly(num_nails, angles)

def angle_to_arc_length(radius, angles_deg):
    angles_rad = np.radians(angles_deg)
    arc_lengths = radius * angles_rad
    return arc_lengths

# Function to plot the relationship between angle and arc length using Plotly
def plot_angle_vs_arc_length_plotly(radius, max_angle):
    angles_deg = np.linspace(0, max_angle, 360*4)
    arc_lengths = angle_to_arc_length(radius, angles_deg)

    fig = go.Figure(data=go.Scatter(x=angles_deg, y=arc_lengths, mode='lines+markers', 
                                    marker=dict(size=5, color='red'), 
                                    hoverinfo='all'))
    
    fig.update_layout(title='Angle vs. Arc Length',
                      xaxis_title='Angle (degrees)',
                      yaxis_title='Arc Length',
                      showlegend=False)
    fig.show()

# Example usage
max_angle = 360  # maximum angle to consider

plot_angle_vs_arc_length_plotly(radius, max_angle)
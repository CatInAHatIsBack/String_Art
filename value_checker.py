import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Load the image
image = Image.open('cropped_and_masked_gray.png')
image = np.array(image)

fig, ax = plt.subplots()

# Display the image
im = ax.imshow(image, cmap='gray')

# Create a text object that will be updated with the current (x, y) and value
txt = fig.text(0.5, 0.5, "", va="bottom", ha="left")

# Create a function to update the text
def hover(event):
    # Check if the mouse is over the image
    if event.inaxes == ax:
        # Get the pixel coordinates
        x, y = int(event.xdata), int(event.ydata)
        # Get the pixel value
        value = image[y, x]
        # Update the text
        txt.set_text(f"x={x}, y={y}, value={value}")

# Connect the function to the hover event
fig.canvas.mpl_connect("motion_notify_event", hover)

# Show the plot
plt.show()

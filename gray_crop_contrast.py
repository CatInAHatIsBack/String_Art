from PIL import Image, ImageEnhance, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider
import numpy as np


path = './human-eye.png'
save = 'gray_crop_contrast_masked2.png'
crop_size = 500

img = Image.open(path)

# grayscale
grayscale_img = img.convert('L')

image = np.array(grayscale_img) 


fig, (ax1, ax2) = plt.subplots(1, 2)
plt.subplots_adjust(bottom=0.25)  # Leave space for slider
im1 = ax1.imshow(image, cmap='gray')
im2 = ax2.imshow(image[:crop_size, :crop_size], cmap='gray')

# This will keep track of the rectangle patch
rect = patches.Rectangle((0,0), crop_size, crop_size, linewidth=1, edgecolor='r', facecolor='none')
ax1.add_patch(rect)

# Add slider for contrast
ax_contrast = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_contrast = Slider(ax_contrast, 'Contrast', 0.1, 5.0, valinit=1.0)

def update_cropped_image(x, y, contrast_factor):
    # Get the cropped image
    cropped = image[y:y+crop_size, x:x+crop_size]
    if cropped.shape[0] != crop_size or cropped.shape[1] != crop_size:
        cropped = np.pad(cropped, ((0, crop_size - cropped.shape[0]), (0, crop_size - cropped.shape[1])), mode='constant')

    # Convert to PIL Image to apply contrast enhancement
    cropped_pil = Image.fromarray(cropped)
    enhancer = ImageEnhance.Contrast(cropped_pil)
    contrasted_cropped = enhancer.enhance(contrast_factor)

    # Set the contrasted cropped image
    im2.set_data(np.array(contrasted_cropped))

def on_move(event):
    if event.inaxes == ax1:
        x, y = int(event.xdata), int(event.ydata)
        if (x < 0 or y < 0 or x >= image.shape[1] or y >= image.shape[0]):
            return
        rect.set_xy((x, y))
        update_cropped_image(x, y, slider_contrast.val)
        fig.canvas.draw()


def on_click(event):
    if event.inaxes == ax1:
        x, y = int(event.xdata), int(event.ydata)
        update_cropped_image(x, y, slider_contrast.val)
        contrasted_cropped = np.array(im2.get_array().data.astype('uint8'))

        mask = Image.new('L', (contrasted_cropped.shape[1], contrasted_cropped.shape[0]), 0)
        y_center, x_center = contrasted_cropped.shape[0] // 2, contrasted_cropped.shape[1] // 2
        radius = min(x_center, y_center)
        ImageDraw.Draw(mask).ellipse((x_center-radius, y_center-radius, x_center+radius, y_center+radius), fill=255)
        mask_np = np.array(mask)

        # Apply the mask
        masked_img = np.where(mask_np==255, contrasted_cropped, 255) # You can change 255 to 0 if you want to make the background black

        # Convert to Image and save
        masked_img_pil = Image.fromarray(np.uint8(masked_img))
        masked_img_pil.save(save)
        print("Image saved as " + save)

def on_slider_update(val):
    # Update the image when the slider value changes
    x, y = rect.xy
    update_cropped_image(int(x), int(y), val)
    fig.canvas.draw_idle()

slider_contrast.on_changed(on_slider_update)

def on_key(event):
    # Only respond to left and right arrow keys
    if event.key == 'left':
        new_val = slider_contrast.val - 0.10
    elif event.key == 'right':
        new_val = slider_contrast.val + 0.10
    else:
        return  # Ignore other keys

    # Clamp the value to the slider's range
    new_val = max(slider_contrast.valmin, min(slider_contrast.valmax, new_val))

    # Update the slider value
    slider_contrast.set_val(new_val)

    # Update the image
    x, y = rect.xy
    update_cropped_image(int(x), int(y), new_val)
    fig.canvas.draw_idle()
    
# Connect the key press event
cid_key = fig.canvas.mpl_connect('key_press_event', on_key)
cid_move = fig.canvas.mpl_connect('motion_notify_event', on_move)
cid_click = fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()

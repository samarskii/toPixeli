import os
from PIL import Image, ImageFilter

# Ensure the 'output' and 'output blurred' directories exist
input_dir = 'output'
output_dir = 'output blurred'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to check if a file is an image
def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))

# Iterate through all files in the 'output' directory
for filename in os.listdir(input_dir):
    if is_image_file(filename):
        # Open an image file
        with Image.open(os.path.join(input_dir, filename)) as img:
            # Apply a blur filter to the image
            blurred_img = img.filter(ImageFilter.GaussianBlur(30))  # Adjust the radius as needed
            
            # Save the blurred image to the 'output blurred' directory
            blurred_img.save(os.path.join(output_dir, filename))

print("Blurring of images is complete.")
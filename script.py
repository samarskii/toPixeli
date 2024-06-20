import random
import os
from PIL import Image, ImageDraw
from rule1 import rule1, SPECIFIC_SEED
from rule2 import rule2, SPECIFIC_SEED

# Set the output directory
OUTPUT_DIRECTORY = "output"
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

# Define flags and parameters for the frame
CREATE_FRAME = True
FRAME_THICKNESS = 8  # Thickness of the frame in pixels

def create_background_canvas(width=128, height=128, background_color='white'):
    total_width = width
    total_height = height
    if CREATE_FRAME:
        total_width += 2 * FRAME_THICKNESS
        total_height += 2 * FRAME_THICKNESS
    
    canvas = Image.new('RGB', (total_width, total_height), background_color)
    
    return canvas

rules = [rule2]
width_height_options = [(16, 16)]

# Generate images
for i in range(5):
    rule_function = random.choice(rules)
    size_option = random.choice(width_height_options)
    img_width = size_option[0]
    img_height = size_option[1]

    # Set a specific seed if specified, else generate a new one
    if SPECIFIC_SEED is not None:
        seed = SPECIFIC_SEED
    else:
        seed = random.randint(1, 1000000000)
        
    random.seed(seed)
        
    canvas = create_background_canvas(img_width, img_height, 'white')
    
    # Draw the main pattern on the inner area
    inner_canvas = Image.new('RGB', (img_width, img_height), 'white')
    rule_function(inner_canvas)
    
    # Add the inner_canvas to the main canvas at the correct position
    if CREATE_FRAME:
        canvas.paste(inner_canvas, (FRAME_THICKNESS, FRAME_THICKNESS))
    else:
        canvas = inner_canvas
    
    # Draw the frame if needed
    if CREATE_FRAME:
        draw = ImageDraw.Draw(canvas)
        for j in range(FRAME_THICKNESS):
            draw.rectangle([j, j, canvas.size[0] - 1 - j, canvas.size[1] - 1 - j], outline='white')
    
    # Resize the canvas
    scale_factor = round(1980 / img_width)
    canvas = canvas.resize((canvas.width * scale_factor, canvas.height * scale_factor), resample=Image.NEAREST)
    rule_index = rules.index(rule_function) + 1
    filename = f"{seed}_{img_width}x{img_height}_{rule_index}.png"
    output_path = os.path.join(OUTPUT_DIRECTORY, filename)
    canvas.save(output_path)
    print(f"Image '{filename}' saved successfully with seed {seed}.")
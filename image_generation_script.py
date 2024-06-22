import random
import os
from PIL import Image, ImageDraw
from rules.rule1 import rule1, SPECIFIC_SEED
from rules.rule2 import rule2
from rules.rule3 import rule3
from rules.rule4 import rule4
from rules.rule5 import rule5
from rules.rule6 import rule6
from rules.rule7 import rule7

# Set the output directory
OUTPUT_DIRECTORY = "output"
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

# Define flags and parameters
CREATE_FRAME = False 
FRAME_THICKNESS = 12
FRAME_COLOR = (255, 255, 255) # White for 255, 255, 255
CREATE_GIF = False  # Set this to False if you don't want to create GIFs

def create_background_canvas(width=128, height=128, background_color='white'):
    total_width = width
    total_height = height
    if CREATE_FRAME:
        total_width += 2 * FRAME_THICKNESS
        total_height += 2 * FRAME_THICKNESS
    canvas = Image.new('RGB', (total_width, total_height), background_color)
    return canvas

def save_gif(images, output_path):
    if not images:
        print(f"No frames captured for GIF: {output_path}")
        return
    try:
        images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
        print(f"GIF saved successfully: {output_path}")
    except Exception as e:
        print(f"Error saving GIF {output_path}: {str(e)}")

def rule_with_capture(rule_function, canvas):
    gif_frames = []
    original_putpixel = canvas.putpixel
    def new_putpixel(*args, **kwargs):
        original_putpixel(*args, **kwargs)
        gif_frames.append(canvas.copy())
    canvas.putpixel = new_putpixel
    rule_function(canvas)
    canvas.putpixel = original_putpixel
    return gif_frames

def generate_image(rule_function, img_width, img_height, seed):
    random.seed(seed)
    canvas = create_background_canvas(img_width, img_height, 'white')
    inner_canvas = Image.new('RGB', (img_width, img_height), 'white')

    if CREATE_GIF:
        gif_frames = rule_with_capture(rule_function, inner_canvas)
    else:
        rule_function(inner_canvas)
        gif_frames = []

    if CREATE_FRAME:
        canvas.paste(inner_canvas, (FRAME_THICKNESS, FRAME_THICKNESS))
        draw = ImageDraw.Draw(canvas)
        for j in range(FRAME_THICKNESS):
            draw.rectangle([j, j, canvas.size[0] - 1 - j, canvas.size[1] - 1 - j], outline=FRAME_COLOR)
    else:
        canvas = inner_canvas

    scale_factor = round(1024*2 / img_width)
    canvas = canvas.resize((canvas.width * scale_factor, canvas.height * scale_factor), resample=Image.NEAREST)

    return canvas, gif_frames

def main():
    rules = [rule1]
    width_height_options = [(61, 34)]

    for i in range(5):
        rule_function = random.choice(rules)
        img_width, img_height = random.choice(width_height_options)
        
        seed = SPECIFIC_SEED if SPECIFIC_SEED is not None else random.randint(1, 1000000000)
        
        canvas, gif_frames = generate_image(rule_function, img_width, img_height, seed)

        rule_index = rules.index(rule_function) + 1
        filename = f"{seed}_{img_width}x{img_height}_{rule_index}.png"
        output_path = os.path.join(OUTPUT_DIRECTORY, filename)
        canvas.save(output_path)
        print(f"Image '{filename}' saved successfully with seed {seed}.")

        if CREATE_GIF and gif_frames:
            gif_filename = f"{seed}_{img_width}x{img_height}_{rule_index}.gif"
            gif_output_path = os.path.join(OUTPUT_DIRECTORY, gif_filename)
            save_gif(gif_frames, gif_output_path)
            print(f"Captured {len(gif_frames)} frames for GIF.")

if __name__ == "__main__":
    main()
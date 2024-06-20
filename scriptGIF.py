import random
import os
from PIL import Image, ImageDraw
from rule1test import get_colors, get_amount_of_first_color, SPECIFIC_SEED, USE_SPECIFIC_SUBRULE, SPECIFIC_SUBRULE

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

def save_gif(images, output_path):
    images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

def rule1_with_capture(canvas, capture_frame):
    colors = get_colors()
    first_color, *colors = colors

    amount_of_first_color = get_amount_of_first_color(canvas)
    first_positions = set()
    min_x, min_y = FRAME_THICKNESS, FRAME_THICKNESS
    max_x, max_y = canvas.size[0] - FRAME_THICKNESS - 1, canvas.size[1] - FRAME_THICKNESS - 1

    while len(first_positions) < amount_of_first_color:
        x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        first_positions.add((x, y))
        canvas.putpixel((x, y), first_color)
        capture_frame(canvas)

    list_of_first_positions = list(first_positions)

    subrules = ["LEFT", "RIGHT", "ABOVE", "BELOW"]
    chosen_subrule = SPECIFIC_SUBRULE if USE_SPECIFIC_SUBRULE else random.choice(subrules)

    if chosen_subrule == 'ABOVE':
        list_of_above_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if y > min_y:
                above_pos = (x, y - 1)
                if above_pos not in list_of_first_positions:
                    list_of_above_positions.append(above_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        left_pos = (x - i, y - 1)
                        right_pos = (x + i, y - 1)
                        if min_x <= left_pos[0] <= max_x and min_y <= left_pos[1] <= max_y and left_pos not in list_of_first_positions:
                            list_of_above_positions.append(left_pos)
                            capture_frame(canvas)
                        if min_x <= right_pos[0] <= max_x and min_y <= right_pos[1] <= max_y and right_pos not in list_of_first_positions:
                            list_of_above_positions.append(right_pos)
                            capture_frame(canvas)

        for i in list_of_above_positions:
            canvas.putpixel(i, colors[0])
            capture_frame(canvas)

    if chosen_subrule == 'BELOW':
        list_of_below_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if y < max_y:
                below_pos = (x, y + 1)
                if below_pos not in list_of_first_positions:
                    list_of_below_positions.append(below_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        left_pos = (x - i, y + 1)
                        right_pos = (x + i, y + 1)
                        if min_x <= left_pos[0] <= max_x and min_y <= left_pos[1] <= max_y and left_pos not in list_of_first_positions:
                            list_of_below_positions.append(left_pos)
                            capture_frame(canvas)
                        if min_x <= right_pos[0] <= max_x and min_y <= right_pos[1] <= max_y and right_pos not in list_of_first_positions:
                            list_of_below_positions.append(right_pos)
                            capture_frame(canvas)

        for i in list_of_below_positions:
            canvas.putpixel(i, colors[0])
            capture_frame(canvas)

    if chosen_subrule == 'RIGHT':
        list_of_right_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x < max_x:
                right_pos = (x + 1, y)
                if right_pos not in list_of_first_positions:
                    list_of_right_positions.append(right_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        above_pos = (x + 1, y - i)
                        below_pos = (x + 1, y + i)
                        if min_x <= above_pos[0] <= max_x and min_y <= above_pos[1] <= max_y and above_pos not in list_of_first_positions:
                            list_of_right_positions.append(above_pos)
                            capture_frame(canvas)
                        if min_x <= below_pos[0] <= max_x and min_y <= below_pos[1] <= max_y and below_pos not in list_of_first_positions:
                            list_of_right_positions.append(below_pos)
                            capture_frame(canvas)

        for i in list_of_right_positions:
            canvas.putpixel(i, colors[0])
            capture_frame(canvas)

    if chosen_subrule == 'LEFT':
        list_of_left_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x > min_x:
                left_pos = (x - 1, y)
                if left_pos not in list_of_first_positions:
                    list_of_left_positions.append(left_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        above_pos = (x - 1, y - i)
                        below_pos = (x - 1, y + i)
                        if min_x <= above_pos[0] <= max_x and min_y <= above_pos[1] <= max_y and above_pos not in list_of_first_positions:
                            list_of_left_positions.append(above_pos)
                            capture_frame(canvas)
                        if min_x <= below_pos[0] <= max_x and min_y <= below_pos[1] <= max_y and below_pos not in list_of_first_positions:
                            list_of_left_positions.append(below_pos)
                            capture_frame(canvas)

        for i in list_of_left_positions:
            canvas.putpixel(i, colors[0])
            capture_frame(canvas)

    amount_of_third_color = round((canvas.size[0] * canvas.size[1]) / random.randint(4, 6) * random.randint(1, 2))
    third_positions = set()
    max_iterations = canvas.size[0] * canvas.size[1]  # Maximum number of iterations
    iteration_count = 0

    while len(third_positions) < amount_of_third_color and iteration_count < max_iterations:
        x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        if canvas.getpixel((x, y)) == (255, 255, 255):
            third_positions.add((x, y))
            canvas.putpixel((x, y), colors[1])
            capture_frame(canvas)
        iteration_count += 1

    try:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if canvas.getpixel((x, y)) == (255, 255, 255):
                    canvas.putpixel((x, y), colors[2])
                    capture_frame(canvas)
    except KeyboardInterrupt:
        print("Program interrupted by the user.")

rules = [rule1_with_capture]
width_height_options = [(16, 16)]

# Generate images
for i in range(3):
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
    gif_frames = []

    def capture_frame(canvas):
        frame = canvas.copy()
        gif_frames.append(frame)

    rule_function(canvas, capture_frame)
    
    if CREATE_FRAME:
        draw = ImageDraw.Draw(canvas)
        for j in range(FRAME_THICKNESS):
            draw.rectangle([j, j, canvas.size[0] - 1 - j, canvas.size[1] - 1 - j], outline='white')
    
    scale_factor = round(1980 / img_width)
    canvas = canvas.resize((canvas.width * scale_factor, canvas.height * scale_factor), resample=Image.NEAREST)
    rule_index = rules.index(rule_function) + 1
    filename = f"{seed}_{img_width}x{img_height}_{rule_index}.png"
    output_path = os.path.join(OUTPUT_DIRECTORY, filename)
    canvas.save(output_path)
    print(f"Image '{filename}' saved successfully with seed {seed}.")

    gif_filename = f"{seed}_{img_width}x{img_height}_{rule_index}.gif"
    gif_output_path = os.path.join(OUTPUT_DIRECTORY, gif_filename)
    save_gif(gif_frames, gif_output_path)
    print(f"GIF '{gif_filename}' saved successfully with seed {seed}.")

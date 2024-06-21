import random
from PIL import Image
from colors.colors4 import pastel_colors_4, vintage_colors_4, retro_colors_4, neon_colors_4, gold_colors_4, light_colors_4   # Correct import statement

# Define specific colors
SPECIFIC_COLORS = [
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (206, 70, 118),   # Pink
    (0, 128, 0),      # Green
    (0, 0, 0)         # Black for border
]

# Flags and parameters
USE_SPECIFIC_COLORS = False  # Change this flag to switch between specific and random colors
USE_RANDOM_AMOUNT = True  # Change this flag to switch between random and specific amount
PARTICULAR_AMOUNT = 40  # Set a particular amount if USE_RANDOM_AMOUNT is False

USE_SPECIFIC_SUBRULE = False  # Change this flag to use a specific subrule
SPECIFIC_SUBRULE = 'ABOVE'   # Set the specific subrule to be used if USE_SPECIFIC_SUBRULE is True

SPECIFIC_SEED = None  # Set a specific seed value for reproducibility, e.g., 42

BORDER_THICKNESS = 0  # Thickness of the colored border in pixels

FROM_COLORS = True  # Flag to use colors from the predefined color lists
COLOR_LIST_NAME = retro_colors_4  # Set the specific color list name if needed

def get_colors():
    if USE_SPECIFIC_COLORS:
        return SPECIFIC_COLORS
    elif FROM_COLORS:
        if COLOR_LIST_NAME:
            color_list = COLOR_LIST_NAME
        else:
            color_list = random.choice(all_colors_lists)
        return [tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for color in random.choice(color_list)]
    else:
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(5)]

def get_amount_of_first_color(canvas):
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(5, 8) * random.randint(1, 2))
    else:
        return PARTICULAR_AMOUNT

def rule1(canvas):
    if SPECIFIC_SEED is not None:
        random.seed(SPECIFIC_SEED)
        
    colors = get_colors()
    first_color, *colors = colors

    amount_of_first_color = get_amount_of_first_color(canvas)
    first_positions = set()
    while len(first_positions) < amount_of_first_color:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        first_positions.add((x, y))
        canvas.putpixel((x, y), first_color)

    list_of_first_positions = list(first_positions)

    subrules = ["LEFT", "RIGHT", "ABOVE", "BELOW"]
    chosen_subrule = SPECIFIC_SUBRULE if USE_SPECIFIC_SUBRULE else random.choice(subrules)

    if chosen_subrule == 'ABOVE':
        list_of_above_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if y > 0:
                above_pos = (x, y - 1)
                if above_pos[1] >= 0 and above_pos not in list_of_first_positions:
                    list_of_above_positions.append(above_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        left_pos = (x - i, y - 1)
                        right_pos = (x + i, y - 1)
                        if (left_pos[0] >= 0 and left_pos[0] < canvas.size[0] and
                                left_pos[1] >= 0 and left_pos[1] < canvas.size[1] and
                                left_pos not in list_of_first_positions):
                            list_of_above_positions.append(left_pos)
                        if (right_pos[0] >= 0 and right_pos[0] < canvas.size[0] and
                                right_pos[1] >= 0 and right_pos[1] < canvas.size[1] and
                                right_pos not in list_of_first_positions):
                            list_of_above_positions.append(right_pos)

        for i in list_of_above_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'BELOW':
        list_of_below_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if y < canvas.size[1] - 1:
                below_pos = (x, y + 1)
                if below_pos[1] < canvas.size[1] and below_pos not in list_of_first_positions:
                    list_of_below_positions.append(below_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        left_pos = (x - i, y + 1)
                        right_pos = (x + i, y + 1)
                        if (left_pos[0] >= 0 and left_pos[0] < canvas.size[0] and
                                left_pos[1] >= 0 and left_pos[1] < canvas.size[1] and
                                left_pos not in list_of_first_positions):
                            list_of_below_positions.append(left_pos)
                        if (right_pos[0] >= 0 and right_pos[0] < canvas.size[0] and
                                right_pos[1] >= 0 and right_pos[1] < canvas.size[1] and
                                right_pos not in list_of_first_positions):
                            list_of_below_positions.append(right_pos)

        for i in list_of_below_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'RIGHT':
        list_of_right_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x < canvas.size[0] - 1:
                right_pos = (x + 1, y)
                if right_pos[0] < canvas.size[0] and right_pos not in list_of_first_positions:
                    list_of_right_positions.append(right_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        above_pos = (x + 1, y - i)
                        below_pos = (x + 1, y + i)
                        if (above_pos[0] < canvas.size[0] and above_pos[0] >= 0 and
                                above_pos[1] < canvas.size[1] and above_pos[1] >= 0 and
                                above_pos not in list_of_first_positions):
                            list_of_right_positions.append(above_pos)
                        if (below_pos[0] < canvas.size[0] and below_pos[0] >= 0 and
                                below_pos[1] < canvas.size[1] and below_pos[1] >= 0 and
                                below_pos not in list_of_first_positions):
                            list_of_right_positions.append(below_pos)

        for i in list_of_right_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'LEFT':
        list_of_left_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x > 0:
                left_pos = (x - 1, y)
                if left_pos[0] >= 0 and left_pos not in list_of_first_positions:
                    list_of_left_positions.append(left_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        above_pos = (x - 1, y - i)
                        below_pos = (x - 1, y + i)
                        if (above_pos[0] >= 0 and above_pos[0] < canvas.size[0] and
                                above_pos[1] >= 0 and above_pos[1] < canvas.size[1] and
                                above_pos not in list_of_first_positions):
                            list_of_left_positions.append(above_pos)
                        if (below_pos[0] >= 0 and below_pos[0] < canvas.size[0] and
                                below_pos[1] >= 0 and below_pos[1] < canvas.size[1] and
                                below_pos not in list_of_first_positions):
                            list_of_left_positions.append(below_pos)

        for i in list_of_left_positions:
            canvas.putpixel(i, colors[0])

    amount_of_third_color = round((canvas.size[0] * canvas.size[1]) / random.randint(4, 6) * random.randint(1, 2))
    third_positions = set()
    max_iterations = canvas.size[0] * canvas.size[1]  # Maximum number of iterations
    iteration_count = 0

    while len(third_positions) < amount_of_third_color and iteration_count < max_iterations:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        if canvas.getpixel((x, y)) == (255, 255, 255):
            third_positions.add((x, y))
            canvas.putpixel((x, y), colors[1])
        iteration_count += 1

    try:
        for x in range(canvas.size[0]):
            for y in range(canvas.size[1]):
                if canvas.getpixel((x, y)) == (255, 255, 255):
                    canvas.putpixel((x, y), colors[2])
                    
    except KeyboardInterrupt:
        print("Program interrupted by the user.")

    # Draw border with the fifth color if BORDER_THICKNESS is greater than 0
    if BORDER_THICKNESS > 0:
        border_color = (0, 0, 0) # Black border color
        for t in range(BORDER_THICKNESS):
            for x in range(canvas.size[0]):
                canvas.putpixel((x, t), border_color)
                canvas.putpixel((x, canvas.size[1] - 1 - t), border_color)
            for y in range(canvas.size[1]):
                canvas.putpixel((t, y), border_color)
                canvas.putpixel((canvas.size[0] - 1 - t, y), border_color)